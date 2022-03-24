import React from "react";

import { Switch } from "components/Switch";
import type { IHeaderConfig } from "components/Table/types";

export const changeVulnTreatmentFormatter = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleOnChange(): void {
    if (key.changeFunction !== undefined) {
      key.changeFunction(row);
    }
  }

  return (
    <Switch
      checked={!("acceptance" in row) || row.acceptance !== "REJECTED"}
      label={{ off: "REJECTED", on: "APPROVED" }}
      onChange={handleOnChange}
    />
  );
};
