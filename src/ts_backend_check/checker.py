# SPDX-License-Identifier: GPL-3.0-or-later
"""
Main module for checking Django models against TypeScript types.
"""

from typing import Dict, List, Tuple

from ts_backend_check.parsers.django_parser import (
    DjangoModelVisitor,
    extract_model_fields,
)
from ts_backend_check.parsers.typescript_parser import TypeScriptParser
from ts_backend_check.utils import is_ordered_subset, snake_to_camel


class TypeChecker:
    """
    Main class for checking Django models against TypeScript types.

    Parameters
    ----------
    models_file : str
        The file path for the models file to check.

    types_file : str
        The file path for the TypeScript interfaces file to check.

    check_blank : bool, default=False
        Whether to also check that fields marked 'blank=True' within Django models are optional (?) in the TypeScript interfaces.

    model_name_conversions : dict[str: list[str]], default={}
        A dictionary containing conversions of model names to their corresponding TypeScript interfaces.
    """

    def __init__(
        self,
        models_file: str,
        types_file: str,
        check_blank: bool = False,
        model_name_conversions: dict[str, list[str]] = {},
    ) -> None:
        self.models_file = models_file
        self.types_file = types_file
        self.check_blank = check_blank
        self.model_name_conversions = model_name_conversions
        self.django_model_visitor = DjangoModelVisitor
        self.model_fields, self.models_and_blank_fields = extract_model_fields(
            models_file
        )
        self.ts_parser = TypeScriptParser(types_file)
        self.ts_interfaces = self.ts_parser.parse_interfaces()
        self.backend_only = self.ts_parser.get_ignored_fields()

    def check(self) -> List[str]:
        """
        Check models against TypeScript types.

        Returns
        -------
        list
            A list of fields missing from the TypeScript file.
        """
        error_fields: list[str] = []

        for model_name, fields in self.model_fields.items():
            missing_fields_exist = False
            interfaces, _ = self._find_matching_interfaces(model_name=model_name)

            if not interfaces:
                error_fields.append(
                    self._format_missing_interface_message(model_name=model_name)
                )
                continue

            for field in fields:
                if not self._field_is_accounted_for(field=field, interfaces=interfaces):
                    error_fields.append(
                        self._format_missing_field_message(
                            field=field, model_name=model_name, interfaces=interfaces
                        )
                    )
                    missing_fields_exist = True

            if self.check_blank and model_name in self.models_and_blank_fields:
                error_fields.extend(
                    self._format_optional_properties_message(
                        field=field,
                        model_name=model_name,
                        models_file=self.models_file,
                        types_file=self.types_file,
                    )
                    for field in self.models_and_blank_fields[model_name]
                    if not self._property_is_optional_when_field_is_blank(
                        model_name=model_name,
                        field=field,
                    )
                )

            if not missing_fields_exist and not self._ts_interface_properties_ordered(
                model_name=model_name, fields=fields
            ):
                error_fields.append(
                    self._format_unordered_interface_properties_message(
                        models_file=self.models_file, types_file=self.types_file
                    )
                )

        return error_fields

    def _find_matching_interfaces(
        self, model_name: str
    ) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
        """
        Find matching TypeScript interfaces for a model.

        Parameters
        ----------
        model_name : str
            The name of the model to check the frontend TypeScript file for.

        Returns
        -------
        Tuple[Dict[str, List[str]], Dict[str, List[str]]]
            Interfaces that match a model name.
        """
        if self.model_name_conversions and model_name in self.model_name_conversions:
            potential_names = self.model_name_conversions[model_name]

        else:
            potential_names = [model_name]

        interfaces = {
            name: interface.properties
            for name, interface in self.ts_interfaces.items()
            if any(potential == name for potential in potential_names)
        }
        interfaces_with_optional_properties = {
            name: interface.optional_properties
            for name, interface in self.ts_interfaces.items()
            if any(potential == name for potential in potential_names)
        }

        return interfaces, interfaces_with_optional_properties

    def _field_is_accounted_for(
        self, field: str, interfaces: Dict[str, List[str]]
    ) -> bool:
        """
        Check if a field is accounted for in TypeScript.

        Parameters
        ----------
        field : str
            The field that should be used in the frontend TypeScript file.

        interfaces : Dict[str, List[str]]
            The interfaces from the frontend TypeScript file.

        Returns
        -------
        Bool
            Whether the field is accounted for in the frontend TypeScript file.
        """
        camel_field = snake_to_camel(input_str=field)
        return (
            camel_field in self.backend_only
            or field in self.backend_only
            or any(camel_field in fields for fields in interfaces.values())
        )

    def _property_is_optional_when_field_is_blank(
        self, model_name: str, field: str
    ) -> bool:
        """
        Check that if the field is 'blank=True' that the corresponding interface property is optional (?).

        Parameters
        ----------
        model_name : str
            The name of the model to check the frontend TypeScript file for.

        field : str
            The field that should match the optional state of the property in the TypeScript file.

        Returns
        -------
        Bool
            Whether the blank status of the model field matches the optional status of the interface property.
        """
        camel_field = snake_to_camel(input_str=field)
        _, interfaces_with_optional_properties = self._find_matching_interfaces(
            model_name
        )

        return any(
            camel_field in properties
            for properties in interfaces_with_optional_properties.values()
        )

    def _ts_interface_properties_ordered(
        self, model_name: str, fields: list[str]
    ) -> bool:
        """
        Check if the order of the TypeScript interface properties exactly matches that of the backend model fields.

        Parameters
        ----------
        model_name : str
            The name of the model to check the frontend TypeScript file for.

        fields : List[str]
            The fields of the backend model.

        Returns
        -------
        bool
            Whether the order of the properties of the TypeScript interface file match that of the backend model fields.
        """
        camel_fields = [snake_to_camel(input_str=f) for f in fields]
        interfaces, _ = self._find_matching_interfaces(model_name)

        return all(
            is_ordered_subset(
                reference_list=camel_fields, candidate_sub_list=interfaces[i]
            )
            for i in interfaces
        )

    @staticmethod
    def _format_missing_interface_message(model_name: str) -> str:
        """
        Format message for missing interface.

        Parameters
        ----------
        model_name : str
            The name of the model that an interface is missing from.

        Returns
        -------
        str
            The message displayed to the user when missing interfaces are found.
        """
        return (
            f"\nNo matching TypeScript interface found for the model '{model_name}'."
            "\nPlease name your TypeScript interfaces the same as the corresponding backend models."
            "\nYou can also use the 'backend_to_ts_model_name_conversions' option within the configuration file."
            "\nThe key is the backend model name and the value is a list of the corresponding interfaces."
            "\nThis option is also how you can break larger backend models into multiple interfaces that extend one another."
        )

    @staticmethod
    def _format_missing_field_message(
        field: str, model_name: str, interfaces: Dict[str, List[str]]
    ) -> str:
        """
        Format message for missing field.

        Parameters
        ----------
        field : str
            The model field that's missing.

        model_name : str
            The name of the model that the field is missing from.

        interfaces : Dict[str, Set[str]]
            The interfaces that have been searched.

        Returns
        -------
        str
            The message displayed to the user when missing fields are found.
        """
        camel_field = snake_to_camel(input_str=field)
        interface_of_interfaces = (
            "interface" if len(interfaces.keys()) == 1 else "interfaces"
        )

        return (
            f"\nField '{field}' (camelCase: '{camel_field}') from model '{model_name}' is missing in the TypeScript interfaces."
            f"\nExpected to find this field in the frontend {interface_of_interfaces}: {', '.join(interfaces.keys())}"
            f"\nTo ignore this field, add the following comment to the TypeScript file (in order based on the model fields): '// ts-backend-check: ignore field {camel_field}'"
        )

    @staticmethod
    def _format_optional_properties_message(
        field: str, model_name: str, models_file: str, types_file: str
    ) -> str:
        """
        Format message for when the blank status of a model field doesn't match the optional status of the corresponding property.

        Parameters
        ----------
        field : str
            The model field that doesn't match blank and optional states.

        model_name : str
            The name of the model that the mismatch occurs in.

        models_file : str
            The file path for the models file to check.

        types_file : str
            The file path for the TypeScript interfaces file that was checked.

        Returns
        -------
        str
            The message displayed to the user when missing fields are found.
        """
        camel_field = snake_to_camel(input_str=field)

        return (
            f"\nField '{field}' (camelCase: '{camel_field}') from model '{model_name}' doesn't match the TypeScript interfaces based on blank to optional agreement."
            f"\nPlease check '{models_file}' and '{types_file}' to make sure that all 'blank=True' fields are optional (?) in the TypeScript interfaces file."
        )

    @staticmethod
    def _format_unordered_interface_properties_message(
        models_file: str, types_file: str
    ) -> str:
        """
        Format message for unordered interface properties.

        Parameters
        ----------
        models_file : str
            The file path for the models file to check.

        types_file : str
            The file path for the TypeScript interfaces file that was checked.

        Returns
        -------
        str
            The message displayed to the user when unordered interface properties are found.
        """
        return (
            f"\nThe properties of the interface file '{types_file}' are unordered."
            f"\nAll interface properties should exactly match the order of the corresponding fields in the '{models_file}' backend model."
            "\nIf the model is synced with multiple interfaces, then their properties should follow the order prescribed by the model fields."
        )
