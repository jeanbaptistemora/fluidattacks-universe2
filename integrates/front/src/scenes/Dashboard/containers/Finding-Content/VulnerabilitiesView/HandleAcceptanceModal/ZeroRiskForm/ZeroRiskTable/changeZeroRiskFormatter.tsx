import React, { useCallback } from "react";

import type { IVulnDataAttr } from "../../types";
import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";

interface IChangeZeroRiskFormatterProps {
  row: IVulnDataAttr;
  approveFunction: (arg1?: IVulnDataAttr | undefined) => void;
  deleteFunction: (arg1?: IVulnDataAttr | undefined) => void;
}
const ChangeZeroRiskFormatter: React.FC<IChangeZeroRiskFormatterProps> = ({
  row,
  approveFunction,
  deleteFunction,
}: IChangeZeroRiskFormatterProps): JSX.Element => {
  const handleOnApprove = useCallback((): void => {
    approveFunction(row);
  }, [approveFunction, row]);

  const handleOnDelete = useCallback((): void => {
    deleteFunction(row);
  }, [deleteFunction, row]);

  return (
    <div style={{ width: "150px" }}>
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
    </div>
  );
};

export const changeZeroRiskFormatter = (
  row: IVulnDataAttr,
  approveFunction: (arg1?: IVulnDataAttr | undefined) => void,
  deleteFunction: (arg1?: IVulnDataAttr | undefined) => void
): JSX.Element => {
  return (
    <ChangeZeroRiskFormatter
      approveFunction={approveFunction}
      deleteFunction={deleteFunction}
      row={row}
    />
  );
};
