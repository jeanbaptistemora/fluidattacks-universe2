import React from "react";

import { StyledContainer } from "./styledComponents";
import type { IContainerProps } from "./types";

const Container: React.FC<IContainerProps> = ({
  align,
  bgColor,
  borderBottomColor,
  borderTopColor,
  borderColor,
  br,
  center,
  children,
  direction,
  display,
  height,
  hoverColor,
  hoverShadow,
  justify,
  justifyMd,
  justifySm,
  leftBar,
  maxWidth,
  mb,
  mh,
  minHeight,
  minWidth,
  minWidthMd,
  minWidthSm,
  ml,
  mr,
  mt,
  mv,
  onClick,
  pb,
  ph,
  phMd,
  phSm,
  pl,
  pr,
  pt,
  pv,
  pvMd,
  pvSm,
  shadow,
  topBar,
  width,
  widthMd,
  widthSm,
  wrap,
}): JSX.Element => {
  return (
    <StyledContainer
      align={align}
      bgColor={bgColor}
      borderBottomColor={borderBottomColor}
      borderColor={borderColor}
      borderTopColor={borderTopColor}
      br={br}
      center={center}
      direction={direction}
      display={display}
      height={height}
      hoverColor={hoverColor}
      hoverShadow={hoverShadow}
      justify={justify}
      justifyMd={justifyMd}
      justifySm={justifySm}
      leftBar={leftBar}
      maxWidth={maxWidth}
      mb={mb}
      mh={mh}
      minHeight={minHeight}
      minWidth={minWidth}
      minWidthMd={minWidthMd}
      minWidthSm={minWidthSm}
      ml={ml}
      mr={mr}
      mt={mt}
      mv={mv}
      onClick={onClick}
      pb={pb}
      ph={ph}
      phMd={phMd}
      phSm={phSm}
      pl={pl}
      pr={pr}
      pt={pt}
      pv={pv}
      pvMd={pvMd}
      pvSm={pvSm}
      shadow={shadow}
      topBar={topBar}
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
