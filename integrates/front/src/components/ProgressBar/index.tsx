/* eslint-disable @typescript-eslint/no-magic-numbers */
import type { FC } from "react";
import React from "react";

import { Bar } from "./styles";

interface IProgressBarProps {
  backgroundColor?: string;
  borderRadius?: number;
  height?: number;
  maxWidth?: number;
  minWidth?: number;
  percentage?: number;
  progressColor?: string;
  width?: number;
}

const getPercentageToDisplay: (percentage: number) => number = (
  percentage: number
): number => {
  if (percentage <= 0) {
    return 0;
  } else if (percentage > 100) {
    return 100;
  }

  return percentage;
};

const ProgressBar: FC<IProgressBarProps> = ({
  backgroundColor = "#DDDDE3",
  borderRadius = 25,
  height = 25,
  maxWidth = 1000,
  minWidth = 30,
  percentage = 98,
  progressColor = "#BF0B1A",
}: Readonly<IProgressBarProps>): JSX.Element => (
  <Bar
    color={backgroundColor}
    display={"inline-block"}
    height={height}
    leftRadius={borderRadius}
    maxWidth={maxWidth}
    minWidth={minWidth}
    rightRadius={borderRadius}
  >
    <Bar
      color={progressColor}
      height={height}
      leftRadius={borderRadius}
      maxWidth={maxWidth}
      minWidth={percentage > 0 ? 5 : 0}
      rightRadius={percentage >= 98 ? borderRadius : 0}
      widthPercentage={getPercentageToDisplay(percentage)}
    />
  </Bar>
);

export type { IProgressBarProps };
export { ProgressBar, getPercentageToDisplay };
