/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import FontAwesome from "react-fontawesome";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

interface ILoginButtonProps {
  className: string;
  fontAwesomeName: string;
  onClick: () => void;
  text: string;
}

const StyledLoginButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 flex ba br0 pa3 mt2 outline-0 justify-between items-center btn-login",
})``;

const LoginButton: React.FC<ILoginButtonProps> = (
  props: Readonly<ILoginButtonProps>
): JSX.Element => {
  const { className, fontAwesomeName, onClick, text } = props;

  return (
    <StyledLoginButton className={className} onClick={onClick}>
      <FontAwesome name={fontAwesomeName} size={"2x"} />
      {text}
    </StyledLoginButton>
  );
};

export { LoginButton };
