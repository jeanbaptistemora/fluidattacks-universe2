import { capitalize } from "lodash";
import React from "react";

import type { IHeaderConfig } from "components/Table/types";
import { TableLink } from "components/TableLink";

export const groupLinkFormatter = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  const groupName = row.name;
  const column = key.dataField;

  return (
    <TableLink
      to={`${groupName.toLowerCase()}/${
        column === "name" ? "vulns" : "events"
      }`}
      value={capitalize(_value.toLocaleLowerCase())}
    />
  );
};
