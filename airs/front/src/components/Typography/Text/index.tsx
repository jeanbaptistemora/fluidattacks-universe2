/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { StyledText } from "./styledComponents";
import type { ITextProps } from "./types";

const Text: React.FC<ITextProps> = ({
  children,
  color,
  display,
  fontStyle,
  hColor,
  mb,
  ml,
  mr,
  mt,
  size,
  textAlign,
  weight,
}: ITextProps): JSX.Element => {
  const MyText = (
    <StyledText
      color={color}
      display={display}
      fontStyle={fontStyle}
      hColor={hColor}
      mb={mb}
      ml={ml}
      mr={mr}
      mt={mt}
      size={size}
      textAlign={textAlign}
      weight={weight}
    >
      {children}
    </StyledText>
  );

  return MyText;
};

export { Text };
