/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
