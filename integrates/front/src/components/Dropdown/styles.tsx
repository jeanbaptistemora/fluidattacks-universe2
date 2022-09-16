/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IDropdownContainerProps {
  align: "center" | "left" | "right";
  bgColor: string;
  zIndex?: number;
}

const sideMap: Record<IDropdownContainerProps["align"], string> = {
  center: `
    left: 50%;
    transform: translateX(-50%);
  `,
  left: "right: 0;",
  right: "left: 0;",
};

const DropdownContainer = styled.div<IDropdownContainerProps>`
  ${({ align }): string => sideMap[align]}
  background-color: ${({ bgColor }): string => bgColor};
  border: 1px solid #c7c7d1;
  border-radius: 4px;
  color: #121216;
  display: none;
  position: absolute;
  top: 100%;
  z-index: ${({ zIndex = 100 }): number => zIndex};
`;

const Wrapper = styled.div.attrs({
  className: "comp-dropdown",
})`
  display: inline-block;
  position: relative;
  :hover > div {
    display: block;
  }
`;

export type { IDropdownContainerProps };
export { DropdownContainer, Wrapper };
