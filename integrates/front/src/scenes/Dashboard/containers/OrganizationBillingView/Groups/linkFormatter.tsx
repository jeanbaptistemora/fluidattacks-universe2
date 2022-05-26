import { capitalize } from "lodash";
import React from "react";

import { LinkRow } from "./lintRow";

import type { IHeaderConfig } from "components/Table/types";
import { translate } from "utils/translations/translate";

export const linkFormatter = (
  value: boolean | string | undefined,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function onClick(): void {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  const valueDefined: boolean | string = value ?? "";
  const formatedValueDefined: string =
    typeof valueDefined === "string"
      ? valueDefined
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
