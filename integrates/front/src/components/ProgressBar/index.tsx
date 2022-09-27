/* eslint-disable @typescript-eslint/no-magic-numbers */
/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC } from "react";
import React from "react";

import { Bar } from "./styles";

interface IProgressBarProps {
  backgroundColor?: string;
  borderRadius?: number;
  height?: number;
  percentage?: number;
  progressColor?: string;
  width?: number;
}

const getPercentageToDisplay: (percentage: number) => number = (
  percentage: number
): number => {
  if (percentage <= 0) {
    return 0;
  } else if (percentage > 0 && percentage <= 1.5) {
    return 1.5;
  } else if (percentage > 100) {
    return 100;
  }

  return percentage;
};

const ProgressBar: FC<IProgressBarProps> = ({
  backgroundColor = "#DDDDE3",
  borderRadius = 25,
  height = 25,
  percentage = 98,
  progressColor = "#BF0B1A",
}: Readonly<IProgressBarProps>): JSX.Element => (
  <Bar
    color={backgroundColor}
    height={height}
    leftRadius={borderRadius}
    rightRadius={borderRadius}
  >
    <Bar
      color={progressColor}
      height={height}
      leftRadius={borderRadius}
      rightRadius={percentage >= 98 ? borderRadius : 0}
      widthPercentage={getPercentageToDisplay(percentage)}
    />
  </Bar>
);

export type { IProgressBarProps };
export { ProgressBar };
