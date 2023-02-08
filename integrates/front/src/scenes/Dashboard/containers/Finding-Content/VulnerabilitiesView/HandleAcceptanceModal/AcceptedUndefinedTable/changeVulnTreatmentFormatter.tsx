import React, { useCallback } from "react";

import type { IVulnDataAttr } from "../types";
import { Switch } from "components/Switch";

interface IChangeVulnTreatmentFormatterProps {
  row: IVulnDataAttr;
  changeFunction: (arg1: IVulnDataAttr) => void;
}

const ChangeVulnTreatmentFormatter: React.FC<IChangeVulnTreatmentFormatterProps> =
  ({
    row,
    changeFunction,
  }: IChangeVulnTreatmentFormatterProps): JSX.Element => {
    const handleOnChange = useCallback((): void => {
      changeFunction(row);
    }, [changeFunction, row]);

    return (
      <Switch
        checked={row.acceptance !== "REJECTED"}
        label={{ off: "REJECTED", on: "APPROVED" }}
        onChange={handleOnChange}
      />
    );
  };

export const changeVulnTreatmentFormatter = (
  row: IVulnDataAttr,
  changeFunction: (arg1: IVulnDataAttr) => void
): JSX.Element => {
  return (
    <ChangeVulnTreatmentFormatter changeFunction={changeFunction} row={row} />
  );
};
