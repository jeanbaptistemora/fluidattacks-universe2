import { capitalize } from "lodash";
import React from "react";

import { LinkRow } from "./lintRow";

import type { IHeaderConfig } from "components/Table/types";

export const linkFormatter = (
  value: string | undefined,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function onClick(): void {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  const formatedValueDefined: string = (value ?? "").replace("_", " ");

  return (
    <LinkRow
      onClick={onClick}
      value={capitalize(formatedValueDefined.toLocaleLowerCase())}
    />
  );
};
