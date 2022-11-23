import React from "react";

import { StyledContainer } from "./styledComponents";
import type { IContainerProps } from "./types";

const Container: React.FC<IContainerProps> = ({
  align,
  bgColor,
  borderBottom,
  borderColor,
  borderTop,
  br,
  center,
  children,
  direction,
  display,
  height,
  justify,
  justifyMd,
  justifySm,
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
  shadow,
  width,
  widthMd,
  widthSm,
  wrap,
}): JSX.Element => {
  return (
    <StyledContainer
      align={align}
      bgColor={bgColor}
      borderBottom={borderBottom}
      borderColor={borderColor}
      borderTop={borderTop}
      br={br}
      center={center}
      direction={direction}
      display={display}
      height={height}
      justify={justify}
      justifyMd={justifyMd}
      justifySm={justifySm}
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
      shadow={shadow}
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
