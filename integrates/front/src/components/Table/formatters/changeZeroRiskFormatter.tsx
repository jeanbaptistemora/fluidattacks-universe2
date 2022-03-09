import React from "react";

import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";
import type { IHeaderConfig } from "components/Table/types";

export const changeZeroRiskFormatter: (
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
  function handleOnApprove(): void {
    if (key.approveFunction !== undefined) {
      key.approveFunction(row);
    }
  }

  function handleOnDelete(): void {
    if (key.deleteFunction !== undefined) {
      key.deleteFunction(row);
    }
  }

  return (
    <MixedCheckBoxButton
      fontSize={"fs-checkbox"}
      id={"zeroRiskCheckBox"}
      isNoEnabled={row.acceptance !== "APPROVED"}
      isSelected={row.acceptance !== ""}
      isYesEnabled={row.acceptance !== "REJECTED"}
      noLabel={row.acceptance === "REJECTED" ? "REJECTED" : "REJECT"}
      onApprove={handleOnApprove}
      onDelete={handleOnDelete}
      yesLabel={row.acceptance === "APPROVED" ? "CONFIRMED" : "CONFIRM"}
    />
  );
};
