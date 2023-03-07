import React from "react";
import type { FC, ReactNode } from "react";

import type { IDropdownContainerProps } from "./styles";
import { DropdownContainer, Wrapper } from "./styles";

import type { IContainerProps } from "components/Container";
import { Container } from "components/Container";

interface IDropdownProps extends Partial<IDropdownContainerProps> {
  button: ReactNode;
  children: ReactNode;
  id?: string;
  maxHeight?: IContainerProps["maxHeight"];
  minWidth?: IContainerProps["minWidth"];
  pb?: IContainerProps["pb"];
  pl?: IContainerProps["pl"];
  pr?: IContainerProps["pr"];
  pt?: IContainerProps["pt"];
}

const Dropdown: FC<IDropdownProps> = ({
  align = "center",
  bgColor = "#f4f4f6",
  border = true,
  button,
  children,
  id,
  maxHeight,
  minWidth = "240px",
  mt,
  pb = "8px",
  pl = "8px",
  pr = "8px",
  pt = "8px",
  shadow = false,
  zIndex = 100,
}: Readonly<IDropdownProps>): JSX.Element => (
  <Wrapper id={id}>
    {button}
    <DropdownContainer
      align={align}
      bgColor={bgColor}
      border={border}
      mt={mt}
      shadow={shadow}
      zIndex={zIndex}
    >
      <Container
        maxHeight={maxHeight}
        minWidth={minWidth}
        pb={pb}
        pl={pl}
        pr={pr}
        pt={pt}
      >
        {children}
      </Container>
    </DropdownContainer>
  </Wrapper>
);

export type { IDropdownProps };
export { Dropdown };
