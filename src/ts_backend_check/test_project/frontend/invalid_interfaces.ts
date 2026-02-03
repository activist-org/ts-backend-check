// SPDX-License-Identifier: GPL-3.0-or-later
export interface Event {
  title: string;
  description: string;
  organizer: User;
  // ts-backend-check: ignore field participants
  isPrivate: boolean;
  // ts-backend-check: ignore field date
}

export interface User {
  id: string;
  name: string;
}
