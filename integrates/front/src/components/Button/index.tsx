/* eslint-disable react/jsx-props-no-spreading
  --------
  We need props spreading in order to pass down props to StyledButton.
*/
import type { ButtonHTMLAttributes } from "react";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

interface IButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant: "primary" | "secondary";
}

const StyledButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className:
      "b--bd b--bh b--orgred ba bg-bd bg-bh bg-transparent cna-bd " +
      "color-bd color-bh hover-white fw100 ml2 orgred " +
      `btn-pa svg-box pointer ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

const Button: React.FC<IButtonProps> = (props): JSX.Element => {
  return <StyledButton {...props} />;
};

export { Button };
