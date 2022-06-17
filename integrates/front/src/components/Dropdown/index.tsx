import React from "react";

import type { IContainerProps } from "./styles";
import { Container, Wrapper } from "./styles";

interface IDropdownProps extends Partial<IContainerProps> {
  button: React.ReactNode;
  children: React.ReactNode;
}

const Dropdown: React.FC<IDropdownProps> = ({
  align = "center",
  button,
  children,
}: Readonly<IDropdownProps>): JSX.Element => (
  <Wrapper>
    {button}
    <Container align={align}>{children}</Container>
  </Wrapper>
);

export type { IDropdownProps };
export { Dropdown };
