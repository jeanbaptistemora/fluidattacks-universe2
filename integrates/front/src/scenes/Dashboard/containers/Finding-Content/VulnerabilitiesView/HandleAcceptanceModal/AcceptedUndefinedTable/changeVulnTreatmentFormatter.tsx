import React from "react";

import type { IVulnDataAttr } from "../types";
import { Switch } from "components/Switch";

export const changeVulnTreatmentFormatter = (
  row: IVulnDataAttr,
  changeFunction: (arg1: IVulnDataAttr) => void
): JSX.Element => {
  function handleOnChange(): void {
    changeFunction(row);
  }

  return (
    <Switch
      checked={row.acceptance !== "REJECTED"}
      label={{ off: "REJECTED", on: "APPROVED" }}
      // eslint-disable-next-line
      onChange={handleOnChange}  // NOSONAR
    />
  );
};
