/* eslint-disable react/jsx-props-no-spreading
  --------
  We need props spreading in order to pass down props to StyledButton.
*/
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const StyledButton: StyledComponent<
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

const TrashButton: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = (
  props: React.ButtonHTMLAttributes<HTMLButtonElement>
): JSX.Element => (
  <StyledButton {...props} type={"button"}>
    <FontAwesomeIcon icon={faTrashAlt} />
  </StyledButton>
);

export { TrashButton };
