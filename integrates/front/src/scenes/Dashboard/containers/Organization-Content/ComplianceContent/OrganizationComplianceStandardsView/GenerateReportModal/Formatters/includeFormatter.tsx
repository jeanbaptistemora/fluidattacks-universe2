import React, { useCallback } from "react";

import type { ITableRowData } from "../types";
import { Switch } from "components/Switch";

interface IIncludeFormatterProps {
  row: ITableRowData;
  changeFunction: (row: ITableRowData) => void;
}

const IncludeFormatter: React.FC<IIncludeFormatterProps> = ({
  row,
  changeFunction,
}: IIncludeFormatterProps): JSX.Element => {
  const handleOnChange: () => void = useCallback((): void => {
    changeFunction(row);
  }, [changeFunction, row]);

  return <Switch checked={row.include} onChange={handleOnChange} />;
};

export const includeFormatter = (
  row: ITableRowData,
  changeFunction: (row: ITableRowData) => void
): JSX.Element => (
  <IncludeFormatter changeFunction={changeFunction} row={row} />
);
