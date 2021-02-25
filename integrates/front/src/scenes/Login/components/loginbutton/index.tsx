/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

interface ILoginButtonProps {
  className: string;
  icon: React.ReactNode;
  id: string;
  onClick: () => void;
  text: string;
}

const StyledLoginButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className:
    "dim w-100 flex ba br0 pa2 outline-0 pointer justify-between items-center btn-login white",
})``;

const LoginButton: React.FC<ILoginButtonProps> = (
  props: Readonly<ILoginButtonProps>
): JSX.Element => {
  const { className, icon, id, onClick, text } = props;

  return (
    <StyledLoginButton className={className} id={id} onClick={onClick}>
      {icon}
      {text}
    </StyledLoginButton>
  );
};

export { LoginButton };
