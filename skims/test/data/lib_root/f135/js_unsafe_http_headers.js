/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { HttpHeaders } from "@angular/common/http";

export class AppComponent {
  login(login) {
    const headers = new HttpHeaders({
      "Content-Type": "application/json",
      "X-XSS-Protection": "anything", // Unsafe F135
      "X-Frame-Options": "anything", // Unsafe F152
    });
  }
}
