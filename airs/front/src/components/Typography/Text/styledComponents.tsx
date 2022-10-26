/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import type { ITextProps } from "./types";

import type { ISize, TSize, TStyle, TWeight } from "../types";

const fontStyles: Record<TStyle, string> = {
  i: "italic",
  no: "normal",
};

const fontWeights: Record<TWeight, number> = {
  bold: 7,
  regular: 4,
  semibold: 6,
};

const sizes: Record<TSize, ISize> = {
  big: { fontSize: "4", lineHeight: "28" },
  medium: { fontSize: "5", lineHeight: "24" },
  small: { fontSize: "6", lineHeight: "22" },
  xs: { fontSize: "7", lineHeight: "22" },
};

const StyledText = styled.p.attrs(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    size = "medium",
    weight = "regular",
  }: ITextProps): {
    className: string;
  } => ({
    className: `f${sizes[size].fontSize} fw${fontWeights[weight]} mb${mb} ml${ml} mr${mr} mt${mt}`,
  })
)<ITextProps>`
  ${({
    color,
    hColor = color,
    display = "block",
    fontStyle = "no",
    textAlign = "start",
    size = "medium",
  }): string => `
    color: ${color};
    display: ${display};
    font-style: ${fontStyles[fontStyle]};
    line-height: ${sizes[size].lineHeight}px;
    text-align: ${textAlign};
    width: ${display === "block" ? "100%" : "auto"};
    :hover {
      color: ${hColor};
    }
  `}
`;

export { StyledText };
