import React, { useCallback } from "react";

import { Switch } from "components/Switch";

interface IChangeVulnStateFormatterProps {
  row: Readonly<Record<string, string>>;
  changeFunction: (arg1: Record<string, string>) => void;
}

const ChangeVulnStateFormatter: React.FC<IChangeVulnStateFormatterProps> = ({
  row,
  changeFunction,
}: IChangeVulnStateFormatterProps): JSX.Element => {
  const handleOnChange = useCallback((): void => {
    changeFunction(row);
  }, [changeFunction, row]);

  return (
    <Switch
      checked={!("state" in row) || row.state !== "SAFE"}
      label={{ off: "Safe", on: "Vulnerable" }}
      onChange={handleOnChange}
    />
  );
};

export const changeVulnStateFormatter = (
  row: Readonly<Record<string, string>>,
  changeFunction: (arg1: Record<string, string>) => void
): JSX.Element => {
  return <ChangeVulnStateFormatter changeFunction={changeFunction} row={row} />;
};
