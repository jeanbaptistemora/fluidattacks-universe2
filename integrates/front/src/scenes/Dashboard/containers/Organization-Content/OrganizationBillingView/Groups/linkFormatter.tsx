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

  function getformatedValue(): string {
    if (typeof valueDefined === "string") {
      return valueDefined.replace("_", " ");
    } else if (valueDefined) {
      return translate.t("organization.tabs.billing.groups.managed.yes");
    }

    return translate.t("organization.tabs.billing.groups.managed.no");
  }

  const formatedValueDefined: string = getformatedValue();

  return (
    <LinkRow
      // eslint-disable-next-line
      onClick={onClick}  // NOSONAR
      value={capitalize(formatedValueDefined.toLocaleLowerCase())}
    />
  );
};
