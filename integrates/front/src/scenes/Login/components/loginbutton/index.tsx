/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
> = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `bn br2 f5 pointer w-100 ${className ?? ""}`,
    type: type ?? "button",
  })
)`
  padding: 1rem 1.5rem;
`;

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
