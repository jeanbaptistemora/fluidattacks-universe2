/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

type TStyle = "i" | "no";
type Nums1To4 = 1 | 2 | 3 | 4;
type Nums1To7 = Nums1To4 | 5 | 6 | 7;
type TWeight = "bold" | "regular" | "semibold";
type TSize = "big" | "medium" | "small" | "xs";

interface ITypographyProps {
  color: string;
  display?: "block" | "inline-block" | "inline";
  hColor?: string;
  mb?: Nums1To7 | 0;
  ml?: Nums1To7 | 0;
  mr?: Nums1To7 | 0;
  mt?: Nums1To7 | 0;
  size?: TSize;
  fontStyle?: TStyle;
  textAlign?: "center" | "end" | "start";
}

interface ISize {
  fontSize: string;
  lineHeight: string;
}

export type { ISize, ITypographyProps, Nums1To4, TSize, TStyle, TWeight };