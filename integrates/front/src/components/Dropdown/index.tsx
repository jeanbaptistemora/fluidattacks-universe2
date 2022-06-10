import React from "react";

import type { IContainerProps } from "./styles";
import { Container, Wrapper } from "./styles";

import { ButtonOpacity } from "components/Button";

interface IDropdownProps extends IContainerProps {
  buttonChildren: React.ReactNode;
  children: React.ReactNode;
}

const Dropdown: React.FC<IDropdownProps> = ({
  align = "center",
  buttonChildren,
  children,
}: Readonly<IDropdownProps>): JSX.Element => (
  <Wrapper>
    <ButtonOpacity>{buttonChildren}</ButtonOpacity>
    <Container align={align}>{children}</Container>
  </Wrapper>
);

export type { IDropdownProps };
export { Dropdown };
