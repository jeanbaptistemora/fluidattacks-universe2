/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import type {
  IContainerProps,
  TAlign,
  TDirection,
  TDisplay,
  TJustify,
  TWrap,
} from "./types";

const getWidth = (defaultWidth: string, width?: string): string =>
  width === undefined ? `width: ${defaultWidth};` : `width: ${width};`;

const getMinWidth = (defaultWidth: string, width?: string): string =>
  width === undefined ? `min-width: ${defaultWidth};` : `min-width: ${width};`;

const getHorizontalMargin = (
  center: boolean,
  mh: number,
  mr: number,
  ml: number
): string => {
  if (center) {
    return `center`;
  } else if (mh !== 0) {
    return `mh${mh}`;
  }

  return `mr${mr} ml${ml}`;
};

const aligns: Record<TAlign, string> = {
  center: "center",
  end: "end",
  start: "start",
  stretch: "stretch",
  unset: "unset",
};

const directions: Record<TDirection, string> = {
  column: "column",
  row: "row",
  unset: "unset",
};

const displays: Record<TDisplay, string> = {
  block: "block",
  flex: "flex",
  ib: "inline-block",
  inline: "inline",
  none: "none",
};

const justifies: Record<TJustify, string> = {
  around: "space-around",
  between: "space-between",
  center: "center",
  end: "flex-end",
  start: "flex-start",
  unset: "unset",
};

const wraps: Record<TWrap, string> = {
  nowrap: "nowrap",
  unset: "unset",
  wrap: "wrap",
};

const StyledContainer = styled.div.attrs<IContainerProps>(
  ({
    br = 0,
    center = false,
    mb = 0,
    mh = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    mv = 0,
    pb = 0,
    ph = 0,
    pl = 0,
    pr = 0,
    pt = 0,
    pv = 0,
  }): {
    className: string;
  } => ({
    className: `
      br${br}
      ${mv === 0 ? `mb${mb} mt${mt}` : `mv${mv}`}
      ${getHorizontalMargin(center, mh, mr, ml)}
      ${pv === 0 ? `pb${pb} pt${pt}` : `pv${pv}`}
      ${ph === 0 ? `pl${pl} pr${pr}` : `ph${ph}`}
    `,
  })
)<IContainerProps>`
  ${({
    align = "unset",
    bgColor = "transparent",
    borderColor = "unset",
    direction = "unset",
    display = "block",
    height = "auto",
    justify = "unset",
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    minWidthMd,
    minWidthSm,
    scroll = "none",
    width = "100%",
    widthMd,
    widthSm,
    wrap = "unset",
  }): string => `
    align-items: ${aligns[align]};
    background-color: ${bgColor};
    border: 1px solid ${borderColor};
    display: ${displays[display]};
    flex-direction: ${directions[direction]};
    flex-wrap: ${wraps[wrap]};
    height: ${height};
    justify-content: ${justifies[justify]};
    max-width: ${maxWidth};
    min-height: ${minHeight};
    overflow-x: ${scroll.includes("x") ? "auto" : "hidden"};
    overflow-y: ${scroll.includes("y") ? "auto" : "hidden"};
    transition: all 0.3s ease;

    @media screen and (min-width: 60em) {
      ${getWidth(width)}
      ${getMinWidth(minWidth)}
    }

    @media screen and (min-width: 30em) and (max-width: 60em) {
      ${getWidth(width, widthMd)}
      ${getMinWidth(minWidth, minWidthMd)}
    }

    @media screen and (max-width: 30em) {
      ${getWidth(widthMd === undefined ? width : widthMd, widthSm)}
      ${getMinWidth(
        minWidthMd === undefined ? minWidth : minWidthMd,
        minWidthSm
      )}
    }
  `}
`;

export { StyledContainer };
