// SPDX-License-Identifier: GPL-3.0-or-later
export interface Event {
  title: string;
  description: string;
  organizer: User;
  participants?: User[];
  // ts-backend-check: ignore field date
}

export interface PrivateEvent extends Event {
  isPrivate: boolean;
}

export interface User {
  id: string;
  name: string;
}
