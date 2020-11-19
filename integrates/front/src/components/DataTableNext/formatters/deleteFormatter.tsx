import { FluidIcon } from "components/FluidIcon";
import type { IHeaderConfig } from "components/DataTableNext/types";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const DeleteFormatter: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs<{
  className: string;
}>({
  className: "b--sb bg-sb svg-box20",
})``;

export const deleteFormatter: (
  value: string,
  row: Readonly<Record<string, string>>,
  rowIndex: number,
  key: Readonly<IHeaderConfig>
) => JSX.Element = (
  _value: string,
  row: Readonly<Record<string, string>>,
  _rowIndex: number,
  key: Readonly<IHeaderConfig>
): JSX.Element => {
  function handleDeleteFormatter(): void {
    if (key.deleteFunction !== undefined) {
      key.deleteFunction(row);
    }
  }

  return (
    <DeleteFormatter onClick={handleDeleteFormatter} type={"button"}>
      <FluidIcon icon={"delete"} />
    </DeleteFormatter>
  );
};
