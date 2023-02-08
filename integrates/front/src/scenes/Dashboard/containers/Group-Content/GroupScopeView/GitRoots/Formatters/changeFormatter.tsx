import React, { useCallback } from "react";

import type { IGitRootData } from "../../types";
import { Switch } from "components/Switch";

interface IChangeFormatterProps {
  row: IGitRootData;
  changeFunction: (arg: IGitRootData) => void;
}

const ChangeFormatter: React.FC<IChangeFormatterProps> = ({
  row,
  changeFunction,
}: IChangeFormatterProps): JSX.Element => {
  const handleOnChange = useCallback((): void => {
    changeFunction(row);
  }, [changeFunction, row]);

  return (
    <Switch
      checked={!("state" in row) || row.state.toUpperCase() !== "INACTIVE"}
      label={{ off: "Inactive", on: "Active" }}
      onChange={handleOnChange}
    />
  );
};

export const changeFormatter = (
  row: IGitRootData,
  changeFunction: (arg: IGitRootData) => void
): JSX.Element => {
  return <ChangeFormatter changeFunction={changeFunction} row={row} />;
};
