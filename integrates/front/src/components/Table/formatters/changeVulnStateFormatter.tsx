import React from "react";

import { SwitchButton } from "components/SwitchButton";
import type { IHeaderConfig } from "components/Table/types";

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
