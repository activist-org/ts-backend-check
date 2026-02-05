// SPDX-License-Identifier: GPL-3.0-or-later
export interface Event {
  // Note: EventModel is mapped to Event and EventExtended via backend_to_ts_model_name_conversions.
  title: string;
  description: string;
  organizer: User;
  participants?: User[];
}

export interface EventExtended extends Event {
  isPrivate: boolean;
  // ts-backend-check: ignore field date
}

export interface User {
  id: string;
  name: string;
}
