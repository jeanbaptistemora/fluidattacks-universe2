import React, { useCallback } from "react";

import type { IOpenRejectCheckBoxProps } from "./types";

import { MixedCheckBoxButton } from "components/MixedCheckBoxButton";

const OpenRejectCheckBox: React.FC<IOpenRejectCheckBoxProps> = (
  props: IOpenRejectCheckBoxProps
): JSX.Element => {
  const { approveFunction, deleteFunction, vulnerabilityRow } = props;

  const handleOnApprove = useCallback((): void => {
    approveFunction(vulnerabilityRow);
  }, [approveFunction, vulnerabilityRow]);

  const handleOnDelete = useCallback((): void => {
    deleteFunction(vulnerabilityRow);
  }, [deleteFunction, vulnerabilityRow]);

  return (
    <React.StrictMode>
      <div style={{ width: "150px" }}>
        <MixedCheckBoxButton
          fontSize={"fs-checkbox"}
          id={"openRejectCheckBox"}
          isNoEnabled={vulnerabilityRow.acceptance !== "APPROVED"}
          isSelected={vulnerabilityRow.acceptance !== ""}
          isYesEnabled={vulnerabilityRow.acceptance !== "REJECTED"}
          noLabel={
            vulnerabilityRow.acceptance === "REJECTED" ? "REJECTED" : "REJECT"
          }
          onApprove={handleOnApprove}
          onDelete={handleOnDelete}
          yesLabel={
            vulnerabilityRow.acceptance === "APPROVED" ? "OPENED" : "OPEN"
          }
        />
      </div>
    </React.StrictMode>
  );
};

export { OpenRejectCheckBox };
