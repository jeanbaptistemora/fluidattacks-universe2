import React from "react";

import type { IHeaderConfig } from "components/DataTableNext/types";
import { SwitchButton } from "components/SwitchButton";

export const changeVulnStateFormatter: (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
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
    <SwitchButton
      checked={!("currentState" in row) || row.currentState !== "closed"}
      id={"vulnStateSwitch"}
      offlabel={"closed"}
      onChange={handleOnChange}
      onlabel={"open"}
    />
  );
};
