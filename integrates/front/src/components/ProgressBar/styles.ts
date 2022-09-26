/* eslint-disable @typescript-eslint/no-magic-numbers */
/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IBarProps {
  color?: string;
  height?: number;
  leftRadius?: number;
  rightRadius?: number;
  widthPercentage?: number;
}

const Bar = styled.div<IBarProps>`
  ${({
    color = "red",
    height = 25,
    leftRadius = 0,
    rightRadius = 0,
    widthPercentage = 100,
  }): string => `
    background-color: ${color};
    width:${widthPercentage}%;
    height:${height}px;
    border-radius: ${leftRadius}px ${rightRadius}px ${rightRadius}px ${leftRadius}px;
  `}
`;

export type { IBarProps };
export { Bar };
