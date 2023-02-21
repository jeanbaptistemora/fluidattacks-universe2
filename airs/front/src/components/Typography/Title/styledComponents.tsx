import styled from "styled-components";

import type { ISize, ITypographyProps, TSize, TStyle } from "../types";

const fontStyles: Record<TStyle, string> = {
  i: "italic",
  no: "normal",
};

const variants: Record<TSize, { sizes: ISize; weight: string }> = {
  big: { sizes: { fontSize: "48px", lineHeight: "56" }, weight: "700" },
  medium: {
    sizes: { fontSize: "36px", lineHeight: "44" },
    weight: "700",
  },
  small: {
    sizes: { fontSize: "24px", lineHeight: "32" },
    weight: "600",
  },
  xs: {
    sizes: { fontSize: "20px", lineHeight: "28" },
    weight: "600",
  },
  xxs: {
    sizes: { fontSize: "16px", lineHeight: "28" },
    weight: "600",
  },
};

const getSize = (defaultSize: TSize, size?: TSize): string =>
  size === undefined
    ? `font-size: ${variants[defaultSize].sizes.fontSize};`
    : `font-size: ${variants[size].sizes.fontSize};`;

const getWeight = (defaultSize: TSize, size?: TSize): string =>
  size === undefined
    ? `font-weight: ${variants[defaultSize].weight};`
    : `font-weight: ${variants[size].weight};`;

const getLineHeight = (defaultSize: TSize, size?: TSize): string =>
  size === undefined
    ? `line-height: ${variants[defaultSize].sizes.lineHeight}px;`
    : `line-height: ${variants[size].sizes.lineHeight}px;`;

const StyledTitle = styled.p.attrs<ITypographyProps>(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
  }): {
    className: string;
  } => ({
    className: `
      mb${mb} ml${ml} mr${mr} mt${mt}
    `,
  })
)<ITypographyProps>`
  ${({
    color,
    hColor = color,
    display = "block",
    fontStyle = "no",
    textAlign = "start",
    size = "medium",
    sizeMd,
    sizeSm,
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

      @media screen and (min-width: 60em) {
        ${getLineHeight(size)}
        ${getSize(size)}
        ${getWeight(size)}
      }

      @media screen and (min-width: 30em) and (max-width: 60em) {
        ${getLineHeight(size, sizeMd)}
        ${getSize(size, sizeMd)}
        ${getWeight(size, sizeMd)}
      }

      @media screen and (max-width: 30em) {
        ${getLineHeight(sizeMd === undefined ? size : sizeMd, sizeSm)}
        ${getSize(sizeMd === undefined ? size : sizeMd, sizeSm)}
        ${getWeight(sizeMd === undefined ? size : sizeMd, sizeSm)}
      }
  `}
`;

export { StyledTitle };
