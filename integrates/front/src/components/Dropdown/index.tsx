/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
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
  padding?: IContainerProps["padding"];
}

const Dropdown: FC<IDropdownProps> = ({
  align = "center",
  bgColor = "#f4f4f6",
  button,
  children,
  id,
  maxHeight,
  minWidth = "240px",
  padding = "8px",
  zIndex = 100,
}: Readonly<IDropdownProps>): JSX.Element => (
  <Wrapper id={id}>
    {button}
    <DropdownContainer align={align} bgColor={bgColor} zIndex={zIndex}>
      <Container maxHeight={maxHeight} minWidth={minWidth} padding={padding}>
        {children}
      </Container>
    </DropdownContainer>
  </Wrapper>
);

export type { IDropdownProps };
export { Dropdown };
