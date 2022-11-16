/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { StyledContainer } from "./styledComponents";
import type { IContainerProps } from "./types";

const Container: React.FC<IContainerProps> = ({
  align,
  bgColor,
  borderColor,
  br,
  center,
  children,
  direction,
  display,
  height,
  justify,
  maxWidth,
  mb,
  mh,
  minHeight,
  minWidth,
  ml,
  mr,
  mt,
  mv,
  pb,
  ph,
  pl,
  pr,
  pt,
  pv,
  width,
  widthMd,
  widthSm,
  wrap,
}): JSX.Element => {
  return (
    <StyledContainer
      align={align}
      bgColor={bgColor}
      borderColor={borderColor}
      br={br}
      center={center}
      direction={direction}
      display={display}
      height={height}
      justify={justify}
      maxWidth={maxWidth}
      mb={mb}
      mh={mh}
      minHeight={minHeight}
      minWidth={minWidth}
      ml={ml}
      mr={mr}
      mt={mt}
      mv={mv}
      pb={pb}
      ph={ph}
      pl={pl}
      pr={pr}
      pt={pt}
      pv={pv}
      width={width}
      widthMd={widthMd}
      widthSm={widthSm}
      wrap={wrap}
    >
      {children}
    </StyledContainer>
  );
};

export { Container };
