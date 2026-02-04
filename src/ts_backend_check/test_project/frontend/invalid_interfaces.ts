// SPDX-License-Identifier: GPL-3.0-or-later
export interface EventModel {
  title: string;
  // description: string; // missing without being ignored
  organizer: User;
  isPrivate: boolean; // unordered based on the backend
  participants: User[]; // not optional
  // ts-backend-check: ignore field date
}

export interface User {
  id: string;
  name: string;
}
