/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import type { ISize, ITypographyProps, TSize, TStyle, TWeight } from "../types";

const fontStyles: Record<TStyle, string> = {
  i: "italic",
  no: "normal",
};

const fontWeights: Record<TWeight, number> = {
  bold: 7,
  regular: 4,
  semibold: 6,
};

const variants: Record<TSize, { sizes: ISize; weight: TWeight }> = {
  big: { sizes: { fontSize: "1", lineHeight: "56" }, weight: "bold" },
  medium: {
    sizes: { fontSize: "2", lineHeight: "44" },
    weight: "bold",
  },
  small: {
    sizes: { fontSize: "3", lineHeight: "32" },
    weight: "semibold",
  },
  xs: {
    sizes: { fontSize: "4", lineHeight: "28" },
    weight: "semibold",
  },
};

const StyledTitle = styled.p.attrs<ITypographyProps>(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    size = "medium",
  }): {
    className: string;
  } => ({
    className: `f${variants[size].sizes.fontSize} fw${
      fontWeights[variants[size].weight]
    } mb${mb} ml${ml} mr${mr} mt${mt}`,
  })
)<ITypographyProps>`
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
        line-height: ${variants[size].sizes.lineHeight}px;
        text-align: ${textAlign};
        width: ${display === "block" ? "100%" : "auto"};
        :hover {
          color: ${hColor};
        }
      `}
`;

export { StyledTitle };
