import React from "react";

import type { IHeaderConfig } from "components/DataTableNext/types";
import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";

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
      isNoEnabled={row.acceptation !== "APPROVED"}
      isSelected={row.acceptation !== ""}
      isYesEnabled={row.acceptation !== "REJECTED"}
      noLabel={row.acceptation === "REJECTED" ? "REJECTED" : "REJECT"}
      onApprove={handleOnApprove}
      onDelete={handleOnDelete}
      yesLabel={row.acceptation === "APPROVED" ? "CONFIRMED" : "CONFIRM"}
    />
  );
};
