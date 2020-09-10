import { FluidIcon } from "components/FluidIcon";
import { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";
import style from "components/DataTableNext/index.css";

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
    <button
      className={style.buttonFormatter}
      onClick={handleDeleteFormatter}
      type={"button"}
    >
      <FluidIcon height={"20px"} icon={"delete"} width={"20px"} />
    </button>
  );
};
