/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { LottieProps } from "react-lottie-player";
import LottiePlayer from "react-lottie-player";
import styled from "styled-components";

type ILottieProps = LottieProps & {
  size?: number;
};

const Lottie = styled(LottiePlayer).attrs(
  ({ play = true }: ILottieProps): ILottieProps => ({
    className: "comp-lottie",
    play,
  })
)<ILottieProps>`
  ${({ size = 16 }): string => `
  height: ${size}px;
  width: ${size}px;
  `}
`;

export { Lottie };
