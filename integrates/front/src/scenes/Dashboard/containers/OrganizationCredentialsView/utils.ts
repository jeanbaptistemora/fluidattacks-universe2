/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ICredentialsAttr } from "./types";

const formatAuthCredentials = (value: ICredentialsAttr): "TOKEN" | "USER" => {
  if (value.isToken) {
    return "TOKEN";
  }

  return "USER";
};
const formatTypeCredentials = (
  value: ICredentialsAttr
): "SSH" | "TOKEN" | "USER" => {
  if (value.type === "HTTPS") {
    return formatAuthCredentials(value);
  }

  return "SSH";
};

export { formatTypeCredentials, formatAuthCredentials };
