// SPDX-License-Identifier: GPL-3.0-or-later
// Note: EventModel is missing a field from models.py.
export interface EventModel {
  title: string;
  organizer: UserModel;
  participants: UserModel[]; // not optional
  isPrivate: boolean;
  // ts-backend-check: ignore field date
}

export interface UserModel {
  name: string; // unordered based on the backend
  id: string;
}
