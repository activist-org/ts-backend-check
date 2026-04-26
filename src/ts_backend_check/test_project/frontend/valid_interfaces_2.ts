// SPDX-License-Identifier: GPL-3.0-or-later
export interface User {
  // Model Fields
  id: string;
  name: string;

  // Inherited Fields
  email?: string;
  password: string;
}
