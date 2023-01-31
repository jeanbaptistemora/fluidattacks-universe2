import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const DeleteFormatter: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `b-sb bg-sb svg-box20 ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

export const deleteFormatter = <T extends object>(
  row: T,
  deleteFunction: (arg?: T) => void
): JSX.Element => {
  function handleDeleteFormatter(
    event: React.FormEvent<HTMLButtonElement>
  ): void {
    event.stopPropagation();
    deleteFunction(row);
  }

  return (
    <DeleteFormatter onClick={handleDeleteFormatter} type={"button"}>
      <FontAwesomeIcon icon={faTrashAlt} />
    </DeleteFormatter>
  );
};
