/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import _ from "lodash";

export const focusError: () => void = (): void => {
  const invalidField: HTMLElement | null =
    document.getElementById("validationError");
  if (!_.isNil(invalidField)) {
    invalidField.scrollIntoView({ behavior: "smooth" });
  }
};
