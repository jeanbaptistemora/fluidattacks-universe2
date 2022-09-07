/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { capitalize } from "lodash";
import React from "react";

import { LinkRow } from "./lintRow";

import { translate } from "utils/translations/translate";

export const linkFormatter = (
  value: boolean | string | undefined,
  row: Readonly<Record<string, string>>,
  changeFunction?: (arg: Record<string, string>) => void
): JSX.Element => {
  function onClick(): void {
    changeFunction?.(row);
  }

  const valueDefined: boolean | string = value ?? "";
  const formatedValueDefined: string =
    typeof valueDefined === "string"
      ? valueDefined.replace("_", " ")
      : valueDefined
      ? translate.t("organization.tabs.billing.groups.managed.yes")
      : translate.t("organization.tabs.billing.groups.managed.no");

  return (
    <LinkRow
      onClick={onClick}
      value={capitalize(formatedValueDefined.toLocaleLowerCase())}
    />
  );
};
