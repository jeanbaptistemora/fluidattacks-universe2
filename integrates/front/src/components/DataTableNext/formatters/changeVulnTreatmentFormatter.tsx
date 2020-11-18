import BootstrapSwitchButton from "bootstrap-switch-button-react";
import { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";

export const changeVulnTreatmentFormatter: (
  value: string,
  row: Readonly<{ [key: string]: string }>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<{ [key: string]: string }>,
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
      checked={!("acceptation" in row) || row.acceptation !== "REJECTED"}
      offlabel={"REJECTED"}
      onChange={handleOnChange}
      onlabel={"APPROVED"}
      onstyle={"danger"}
      // Disable to apply custom styles to the switch button.
      // eslint-disable-next-line react/forbid-component-props, react/style-prop-object
      style={"btn-block"}
    />
  );
};
