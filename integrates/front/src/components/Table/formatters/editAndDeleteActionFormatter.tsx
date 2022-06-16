import { faPen, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import type { IHeaderConfig } from "components/Table/types";

const ActionButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  (): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: "b--sb bg-sb svg-box20",
  })
)`
  cursor: pointer;
`;
const Row: StyledComponent<"div", Record<string, unknown>> = styled.div.attrs<{
  className: string;
}>({
  className: "flex",
})``;

export const editAndDeleteActionFormatter: (
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
  function handleDelete(event: React.FormEvent<HTMLButtonElement>): void {
    if (key.deleteFunction !== undefined) {
      event.stopPropagation();
      key.deleteFunction(row);
    }
  }

  function handleEdit(event: React.FormEvent<HTMLButtonElement>): void {
    if (key.editFunction !== undefined) {
      event.stopPropagation();
      key.editFunction(row);
    }
  }

  return (
    <Row>
      <ActionButton onClick={handleEdit}>
        <FontAwesomeIcon icon={faPen} />
      </ActionButton>
      <ActionButton onClick={handleDelete}>
        <FontAwesomeIcon icon={faTrashAlt} />
      </ActionButton>
    </Row>
  );
};
