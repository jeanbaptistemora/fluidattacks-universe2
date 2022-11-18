/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const SlideContainer = styled.div.attrs({
  className: `
      center
    `,
})<{ initialWidth: number }>`
  ${({ initialWidth }): string => {
    return `
      width: ${initialWidth}px;

      @media screen and (max-width: 1504px) {
        width: ${initialWidth - 360}px;
      }

      @media screen and (max-width: 1144px) {
        width: ${initialWidth - 360 * 2}px;
      }

      @media screen and (max-width: 784px) {
        width: ${
          initialWidth - 360 * 3 === 0
            ? initialWidth - 360 * 2
            : initialWidth - 360 * 3
        }px;
      }

      @media screen and (max-width: 30em) {
        width: 286px;
      }
  `;
  }}
`;

export { SlideContainer };
