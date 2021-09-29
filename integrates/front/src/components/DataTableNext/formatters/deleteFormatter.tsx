import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import type { IHeaderConfig } from "components/DataTableNext/types";

const DeleteFormatter: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `b--sb bg-sb svg-box20 ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

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
  function handleDeleteFormatter(
    event: React.FormEvent<HTMLButtonElement>
  ): void {
    if (key.deleteFunction !== undefined) {
      event.stopPropagation();
      key.deleteFunction(row);
    }
  }

  return (
    <DeleteFormatter onClick={handleDeleteFormatter} type={"button"}>
      <FontAwesomeIcon icon={faTrashAlt} />
    </DeleteFormatter>
  );
};
