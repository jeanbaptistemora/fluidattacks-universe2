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
  xxs: { fontSize: "7", lineHeight: "22" },
};

const getSize = (size: TSize, sizeMd?: TSize, sizeSm?: TSize): string => {
  if (sizeMd && sizeSm) {
    return `f${sizes[size].fontSize}-l f${sizes[sizeMd].fontSize}-m f${sizes[sizeSm].fontSize}`;
  } else if (sizeMd) {
    return `f${sizes[size].fontSize}-l f${sizes[sizeMd].fontSize}`;
  } else if (sizeSm) {
    return `f${sizes[size].fontSize}-ns f${sizes[sizeSm].fontSize}`;
  }

  return `f${sizes[size].fontSize}`;
};

const getLineHeight = (defaultSize: TSize, size?: TSize): string =>
  size === undefined
    ? `line-height: ${sizes[defaultSize].lineHeight}px;`
    : `line-height: ${sizes[size].lineHeight}px;`;

const StyledText = styled.p.attrs<ITextProps>(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    size = "medium",
    sizeMd,
    sizeSm,
    weight = "regular",
  }): {
    className: string;
  } => ({
    className: `${getSize(size, sizeMd, sizeSm)} fw${
      fontWeights[weight]
    } mb${mb} ml${ml} mr${mr} mt${mt}`,
  })
)<ITextProps>`
  ${({
    color,
    hColor = color,
    display = "block",
    fontStyle = "no",
    textAlign = "unset",
    size = "medium",
    sizeMd,
    sizeSm,
  }): string => `
    color: ${color};
    display: ${display};
    font-style: ${fontStyles[fontStyle]};
    text-align: ${textAlign};
    width: ${display === "block" ? "100%" : "auto"};
    :hover {
      color: ${hColor};
    }

    @media screen and (min-width: 60em) {
      ${getLineHeight(size)}
    }

    @media screen and (min-width: 30em) and (max-width: 60em) {
      ${getLineHeight(size, sizeMd)}
    }

    @media screen and (max-width: 30em) {
      ${getLineHeight(sizeMd === undefined ? size : sizeMd, sizeSm)}
    }
  `}
`;

export { StyledText };
