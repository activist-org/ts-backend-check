# Changelog

See the [releases for ts-backend-check](https://github.com/activist-org/ts-backend-check/releases) for an up to date list of versions and their release dates.

`ts-backend-check` tries to follow [semantic versioning](https://semver.org/), a MAJOR.MINOR.PATCH version where increments are made of the:

- MAJOR version when we make incompatible API changes
- MINOR version when we add functionality in a backwards compatible manner
- PATCH version when we make backwards compatible bug fixes

Emojis for the following are chosen based on [gitmoji](https://gitmoji.dev/).

## [Upcoming] ts-backend-check 1.x

### ✨ Features

- Adds the ability for the user to check the most recent version of the package via the CLI's version command and upgrade it via a simple CLI argument ([#12](https://github.com/activist-org/ts-backend-check/issues/12)).
- The outputs of the CLI are colored using [Rich](https://github.com/Textualize/rich) ([#10](https://github.com/activist-org/ts-backend-check/issues/10)).

### ⬆️ Dependencies

- Dependencies were updated due to detected vulnerabilities.

## ts-backend-check 1.1.0

### ✨ Features

- An argparse based CLI was developed ([#7](https://github.com/activist-org/ts-backend-check/issues/7)) to help check TypeScript types against their corresponding backend models.
  - Arguments include passing a backend model file and a TypeScript file that should be compared.
  - The backend model fields are extracted, which currently works for Django based models.
  - These model fields are then compared against a TypeScript file to check if they have been mentioned in the code.
  - This process helps keep frontend and backend development processes in sync.

### 🎨 Design

- A logo and icon have been designed for the package.

### ⚖️ Legal

- The code has been appropriately licensed and includes SPDX license identifiers in all files.
- A security file has been added to the repo to make steps clear.

### ✅ Tests

- Testing has been written for the CLI functionalities ([#2](https://github.com/activist-org/ts-bachend-check/issues/2)).
- GitHub Actions based checks are used to validate file license headers, ruff based code formatting, mypy static type checking and pytest based tests on each pull request.
- pre-commit hooks are used to enforce code quality before commits during development.

### 📝 Documentation

- All onboarding documentation has been written including an extensive readme, a contributing guide and GitHub templates to help people contribute effectively.
- Read the Docs documentation has been generated for the project and can be found at [ts-backend-check.readthedocs.io](https://ts-backend-check.readthedocs.io/en/latest/) ([#3](https://github.com/activist-org/ts-bachend-check/issues/3)).
- All docstrings for functions and classes were standardized based on numpydoc.

### ♻️ Code Refactoring

- Code originally developed in the [activist-org/activist](https://github.com/activist-org/activist) project was moved to a separate repo.
