import React from "react";

import { ConfirmVulnerabilityCheckBox } from "./ConfirmVulnerabilityCheckBox";

import type { IVulnDataAttr } from "../../types";

export const changeSubmittedFormatter = (
  row: IVulnDataAttr,
  approveFunction: (arg1?: IVulnDataAttr | undefined) => void,
  deleteFunction: (arg1?: IVulnDataAttr | undefined) => void
): JSX.Element => {
  return (
    <ConfirmVulnerabilityCheckBox
      approveFunction={approveFunction}
      deleteFunction={deleteFunction}
      vulnerabilityRow={row}
    />
  );
};
