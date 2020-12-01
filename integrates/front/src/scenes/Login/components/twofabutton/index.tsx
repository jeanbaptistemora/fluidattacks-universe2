/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import FontAwesome from "react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

interface ITwoFaButtonProps {
  className: string;
  fontAwesomeName: string;
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
  const { className, fontAwesomeName, onClick } = props;

  return (
    <StyledTwoFaButton className={className} onClick={onClick}>
      <span>
        <FontAwesome name={fontAwesomeName} size={"2x"} />
      </span>
    </StyledTwoFaButton>
  );
};

export { TwoFaButton };
