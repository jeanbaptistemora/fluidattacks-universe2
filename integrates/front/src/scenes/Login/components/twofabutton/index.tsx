/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

interface ITwoFaButtonProps {
  className: string;
  icon: React.ReactNode;
  onClick: () => void;
}

const StyledTwoFaButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: "dim w-100 db ba br0 outline-0",
})``;

const TwoFaButton: React.FC<ITwoFaButtonProps> = (
  props: Readonly<ITwoFaButtonProps>
): JSX.Element => {
  const { className, icon, onClick } = props;

  return (
    <StyledTwoFaButton className={className} onClick={onClick}>
      {icon}
    </StyledTwoFaButton>
  );
};

export { TwoFaButton };
