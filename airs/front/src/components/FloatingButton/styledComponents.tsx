/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const FloatButton = styled.div.attrs({
  className: `
    f5
    br2
    dib
    poppins
    pointer
    t-all-3-eio
  `,
})<{ bgColor: string; color: string; yPosition: string }>`
  top: ${({ yPosition }): string => yPosition};
  color: ${({ color }): string => color};
  opacity: 0.9;
  right: -70px;
  height: 100px;
  position: fixed;
  padding: 10px 16px;
  transform: rotate(270deg);
  background-color: ${({ bgColor }): string => bgColor};

  :hover {
    opacity: 1;
    right: -50px;
  }
`;

export { FloatButton };
