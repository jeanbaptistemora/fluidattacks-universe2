import React from "react";

import { OpenRejectCheckBox } from "./OpenRejectCheckBox";

import type { IVulnDataAttr } from "../types";

export const changeSubmittedFormatter = (
  row: IVulnDataAttr,
  approveFunction: (arg1?: IVulnDataAttr | undefined) => void,
  deleteFunction: (arg1?: IVulnDataAttr | undefined) => void
): JSX.Element => {
  return (
    <OpenRejectCheckBox
      approveFunction={approveFunction}
      deleteFunction={deleteFunction}
      vulnerabilityRow={row}
    />
  );
};
