import React from "react";

import type { IHeaderConfig } from "components/DataTableNext/types";
import { SwitchButton } from "components/SwitchButton";

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
