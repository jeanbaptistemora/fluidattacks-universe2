import React from "react";

import { SwitchButton } from "components/SwitchButton";
import type { IHeaderConfig } from "components/Table/types";

export const changeZeroRiskRejectionFormatter: (
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
      checked={row.acceptance === "REJECTED"}
      fontSize={"cr-switch"}
      id={"zeroRiskRejectionSwitch"}
      offlabel={"NON REJECTED"}
      onChange={handleOnChange}
      onlabel={"REJECTED"}
      switchColor={"red-switch"}
    />
  );
};
