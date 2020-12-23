import BootstrapSwitchButton from "bootstrap-switch-button-react";
import type { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";

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
    <BootstrapSwitchButton
      checked={row.acceptation === "REJECTED"}
      offlabel={"NON REJECTED"}
      offstyle={"outline-light"}
      onChange={handleOnChange}
      onlabel={"REJECTED"}
      onstyle={"danger"}
      // Disable to apply custom styles to the switch button.
      // eslint-disable-next-line react/forbid-component-props, react/style-prop-object
      style={"btn-block"}
    />
  );
};
