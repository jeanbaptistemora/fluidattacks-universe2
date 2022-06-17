import React from "react";

import type { IDropdownContainerProps } from "./styles";
import { DropdownContainer, Wrapper } from "./styles";

import type { IContainerProps } from "components/Container";
import { Container } from "components/Container";

interface IDropdownProps extends Partial<IDropdownContainerProps> {
  button: React.ReactNode;
  children: React.ReactNode;
  maxHeight?: IContainerProps["maxHeight"];
  minWidth?: IContainerProps["minWidth"];
  padding?: IContainerProps["padding"];
}

const Dropdown: React.FC<IDropdownProps> = ({
  align = "center",
  button,
  children,
  maxHeight,
  minWidth = "240px",
  padding = "8px",
}: Readonly<IDropdownProps>): JSX.Element => (
  <Wrapper>
    {button}
    <DropdownContainer align={align}>
      <Container maxHeight={maxHeight} minWidth={minWidth} padding={padding}>
        {children}
      </Container>
    </DropdownContainer>
  </Wrapper>
);

export type { IDropdownProps };
export { Dropdown };
