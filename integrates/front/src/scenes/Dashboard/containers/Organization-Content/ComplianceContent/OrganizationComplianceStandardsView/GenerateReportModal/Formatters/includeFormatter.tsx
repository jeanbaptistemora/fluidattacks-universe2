import React, { useCallback } from "react";

import type { IUnfulfilledStandardData } from "../types";
import { Switch } from "components/Switch";

interface IIncludeFormatterProps {
  row: IUnfulfilledStandardData;
  changeFunction: (row: IUnfulfilledStandardData) => void;
}

const IncludeFormatter: React.FC<IIncludeFormatterProps> = ({
  row,
  changeFunction,
}: IIncludeFormatterProps): JSX.Element => {
  const handleOnChange: () => void = useCallback((): void => {
    changeFunction(row);
  }, [changeFunction, row]);

  return (
    <Switch
      checked={row.include}
      label={{ off: "Exclude", on: "Include" }}
      onChange={handleOnChange}
    />
  );
};

export const includeFormatter = (
  row: IUnfulfilledStandardData,
  changeFunction: (row: IUnfulfilledStandardData) => void
): JSX.Element => (
  <IncludeFormatter changeFunction={changeFunction} row={row} />
);
