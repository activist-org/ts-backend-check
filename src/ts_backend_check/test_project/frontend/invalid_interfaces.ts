// SPDX-License-Identifier: GPL-3.0-or-later
// Attn: EventModel is missing a field from backend/models.py.
export interface Event {
  // Note: EventModel is mapped to Event and EventExtended via backend_to_ts_model_name_conversions.
  title: string;
  organizer: User;
  // Attn: participants is not optional.
  participants: User[];
}

export interface EventExtended extends Event {
  // Attn: date is out of order below, but this won't be reported as we have missing fields.
  // ts-backend-check: ignore date
  isPrivate: boolean;
}

// Attn: User is not synced to UserModel via backend_to_ts_model_name_conversions.
export interface User {
  id: string;
  name: string;
}
