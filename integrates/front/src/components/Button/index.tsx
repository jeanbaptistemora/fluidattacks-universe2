/* eslint-disable react/jsx-props-no-spreading
  --------
  We need props spreading in order to pass down props to StyledButton.
*/
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const StyledButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs(
  (
    props: React.ButtonHTMLAttributes<HTMLButtonElement>
  ): {
    className: string;
    type: "submit" | "reset" | "button";
  } => ({
    className:
      "b--bd b--bh b--orgred ba bg-bd bg-bh bg-btn cna-bd color-bd color-bh hover-white " +
      "fw100 ml2 montserrat orgred btn-pa svg-box",
    type: props.type ?? "button",
  })
)``;

const Button: React.FC<React.ButtonHTMLAttributes<HTMLButtonElement>> = (
  props: React.ButtonHTMLAttributes<HTMLButtonElement>
): JSX.Element => {
  return <StyledButton {...props} />;
};

export { Button };
