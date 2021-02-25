import type { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";
import { SwitchButton } from "components/SwitchButton";

export const changeFormatter: (
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
      checked={!("state" in row) || row.state.toUpperCase() !== "INACTIVE"}
      id={"rootSwitch"}
      offlabel={"Inactive"}
      onChange={handleOnChange}
      onlabel={"Active"}
    />
  );
};
