import styled from "styled-components";

import type { ISize, ITypographyProps, TSize, TStyle, TWeight } from "../types";

const fontStyles: Record<TStyle, string> = {
  i: "italic",
  no: "normal",
};

const fontWeights: Record<TWeight, number> = {
  bold: 7,
  regular: 4,
  semibold: 6,
};

const variants: Record<TSize, { sizes: ISize; weight: TWeight }> = {
  big: { sizes: { fontSize: "1", lineHeight: "56" }, weight: "bold" },
  medium: {
    sizes: { fontSize: "2", lineHeight: "44" },
    weight: "bold",
  },
  small: {
    sizes: { fontSize: "3", lineHeight: "32" },
    weight: "semibold",
  },
  xs: {
    sizes: { fontSize: "4", lineHeight: "28" },
    weight: "semibold",
  },
  xxs: {
    sizes: { fontSize: "5", lineHeight: "28" },
    weight: "semibold",
  },
};

const getSize = (size: TSize, sizeMd?: TSize, sizeSm?: TSize): string => {
  if (sizeMd && sizeSm) {
    return `
      f${variants[size].sizes.fontSize}-l
      f${variants[sizeMd].sizes.fontSize}-m
      f${variants[sizeSm].sizes.fontSize}
      fw${fontWeights[variants[size].weight]}-l
      fw${fontWeights[variants[sizeMd].weight]}-m
      fw${fontWeights[variants[sizeSm].weight]}
    `;
  } else if (sizeMd) {
    return `
      f${variants[size].sizes.fontSize}-l
      f${variants[sizeMd].sizes.fontSize}
      fw${fontWeights[variants[size].weight]}-l
      fw${fontWeights[variants[sizeMd].weight]}
    `;
  } else if (sizeSm) {
    return `
      f${variants[size].sizes.fontSize}-ns
      f${variants[sizeSm].sizes.fontSize}
      fw${fontWeights[variants[size].weight]}-ns
      fw${fontWeights[variants[sizeSm].weight]}
    `;
  }

  return `
    f${variants[size].sizes.fontSize}
    fw${fontWeights[variants[size].weight]}
  `;
};

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
    size = "medium",
    sizeMd,
    sizeSm,
  }): {
    className: string;
  } => ({
    className: `
      ${getSize(size, sizeMd, sizeSm)}
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
      }

      @media screen and (min-width: 30em) and (max-width: 60em) {
        ${getLineHeight(size, sizeMd)}
      }

      @media screen and (max-width: 30em) {
        ${getLineHeight(sizeMd === undefined ? size : sizeMd, sizeSm)}
      }
  `}
`;

export { StyledTitle };
