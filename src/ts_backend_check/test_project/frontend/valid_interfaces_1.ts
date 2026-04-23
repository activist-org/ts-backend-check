// SPDX-License-Identifier: GPL-3.0-or-later
import type { User } from "./valid_interfaces_2.ts";

export interface Event {
  // Note: EventModel is mapped to Event and EventExtended via backend_to_ts_model_name_conversions.
  title: string;
  description: string;
  organizer: User;
  participants?: User[];
}

export interface EventExtended extends Event {
  isPrivate: boolean;
  // tsbc: ignore date
}
