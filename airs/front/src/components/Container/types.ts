/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

type Nums0To4 = 0 | 1 | 2 | 3 | 4;
type Nums0To7 = Nums0To4 | 5 | 6 | 7;
type TAlign = "center" | "end" | "start" | "stretch" | "unset";
type TDirection = "column" | "row" | "unset";
type TDisplay = "block" | "flex" | "ib" | "inline" | "none";
type TJustify = "around" | "between" | "center" | "end" | "start" | "unset";
type TWrap = "nowrap" | "unset" | "wrap";

interface IContainerProps {
  align?: TAlign;
  bgColor?: string;
  borderColor?: string;
  br?: Nums0To4;
  center?: boolean;
  children: React.ReactNode;
  direction?: TDirection;
  display?: TDisplay;
  height?: string;
  justify?: TJustify;
  mv?: Nums0To7;
  mh?: Nums0To7;
  pv?: Nums0To7;
  ph?: Nums0To7;
  mb?: Nums0To7;
  ml?: Nums0To7;
  mr?: Nums0To7;
  mt?: Nums0To7;
  pb?: Nums0To7;
  pl?: Nums0To7;
  pr?: Nums0To7;
  pt?: Nums0To7;
  maxWidth?: string;
  minHeight?: string;
  minWidth?: string;
  width?: string;
  widthMd?: string;
  widthSm?: string;
  wrap?: TWrap;
}

export type { IContainerProps, TAlign, TDirection, TDisplay, TJustify, TWrap };
