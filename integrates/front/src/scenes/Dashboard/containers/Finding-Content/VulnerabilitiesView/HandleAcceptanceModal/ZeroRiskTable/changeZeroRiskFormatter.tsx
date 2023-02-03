import React from "react";

import type { IVulnDataAttr } from "../types";
import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";

export const changeZeroRiskFormatter = (
  row: IVulnDataAttr,
  approveFunction: (arg1?: IVulnDataAttr | undefined) => void,
  deleteFunction: (arg1?: IVulnDataAttr | undefined) => void
): JSX.Element => {
  function handleOnApprove(): void {
    approveFunction(row);
  }

  function handleOnDelete(): void {
    deleteFunction(row);
  }

  return (
    <div style={{ width: "150px" }}>
      <MixedCheckBoxButton
        fontSize={"fs-checkbox"}
        id={"zeroRiskCheckBox"}
        isNoEnabled={row.acceptance !== "APPROVED"}
        isSelected={row.acceptance !== ""}
        isYesEnabled={row.acceptance !== "REJECTED"}
        noLabel={row.acceptance === "REJECTED" ? "REJECTED" : "REJECT"}
        // eslint-disable-next-line
        onApprove={handleOnApprove} // NOSONAR
        // eslint-disable-next-line
        onDelete={handleOnDelete} // NOSONAR
        yesLabel={row.acceptance === "APPROVED" ? "CONFIRMED" : "CONFIRM"}
      />
    </div>
  );
};
