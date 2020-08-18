import { FluidIcon } from "../../FluidIcon";
import { IHeaderConfig } from "../types";
import React from "react";
import style from "../index.css";

export const approveFormatter: (
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
  function handleApproveFormatter(): void {
    if (key.approveFunction !== undefined) {
      key.approveFunction(row);
    }
  }

  return (
    <button
      className={style.buttonFormatter}
      onClick={handleApproveFormatter}
      type={"button"}
    >
      <FluidIcon height={"20px"} icon={"verified"} width={"20px"} />
    </button>
  );
};
