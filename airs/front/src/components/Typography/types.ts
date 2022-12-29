import type React from "react";

type TStyle = "i" | "no";
type Nums1To4 = 1 | 2 | 3 | 4;
type Nums1To7 = Nums1To4 | 5 | 6 | 7;
type TWeight = "bold" | "regular" | "semibold";
type TSize = "big" | "medium" | "small" | "xs";

interface ITypographyProps {
  color: string;
  children: React.ReactNode;
  display?: "block" | "inline-block" | "inline";
  hColor?: string;
  mb?: Nums1To7 | 0;
  ml?: Nums1To7 | 0;
  mr?: Nums1To7 | 0;
  mt?: Nums1To7 | 0;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
  fontStyle?: TStyle;
  textAlign?: "center" | "end" | "start" | "unset";
}

interface ISize {
  fontSize: string;
  lineHeight: string;
}

export type { ISize, ITypographyProps, Nums1To4, TSize, TStyle, TWeight };
