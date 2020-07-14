import { FluidIcon } from "../../FluidIcon";
import { IHeaderConfig } from "../types";
import React from "react";

export const deleteFormatter: (
  value: string,
  row: Readonly<{ [key: string]: string }>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<{ [key: string]: string }>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleDeleteFormatter(): void {
    if (key.deleteFunction !== undefined) {
      key.deleteFunction(row);
    }
  }

  return (
    <a onClick={handleDeleteFormatter}>
      <FluidIcon height={"20px"} icon={"delete"} width={"20px"} />
    </a>
  );
};
