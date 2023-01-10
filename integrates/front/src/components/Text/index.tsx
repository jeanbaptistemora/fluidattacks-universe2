import styled from "styled-components";

type TColor = "dark" | "light" | "red";
type TDecor = "over" | "through" | "under";
type TStyle = "i" | "no";
type Nums1To7 = 1 | 2 | 3 | 4 | 5 | 6 | 7;
type Nums1To9 = Nums1To7 | 8 | 9;
type TSize = "big" | "medium" | "small" | "xs";

interface ITextProps {
  bright?: Nums1To9 | 0;
  decor?: TDecor[];
  disp?: "block" | "inline-block" | "inline";
  fontSize?: string;
  hoverBright?: Nums1To9 | 0;
  hoverTone?: TColor;
  mb?: Nums1To7 | 0;
  ml?: Nums1To7 | 0;
  mr?: Nums1To7 | 0;
  mt?: Nums1To7 | 0;
  size?: TSize;
  tone?: TColor;
  fs?: TStyle;
  fw?: Nums1To9;
  ta?: "center" | "end" | "start";
  ws?: "break-spaces" | "normal" | "nowrap" | "pre-line" | "pre-wrap" | "pre";
}

const colors: Record<TColor, string[]> = {
  dark: [
    "121216",
    "1c1c22",
    "25252d",
    "2e2e38",
    "373743",
    "40404f",
    "49495a",
    "535365",
    "5c5c70",
    "65657b",
  ],
  light: [
    "f4f4f6",
    "e9e9ed",
    "dddde3",
    "d2d2da",
    "c7c7d1",
    "bcbcc8",
    "b0b0bf",
    "a5a5b6",
    "9a9aac",
    "8f8fa3",
  ],
  red: [
    "bf0b1a",
    "d40c1d",
    "e70d20",
    "f2182a",
    "f32b3c",
    "fa9ea3",
    "fbb1b5",
    "fcc5c8",
    "fdd8da",
    "feeced",
  ],
};

const decors: Record<TDecor, string> = {
  over: "overline",
  through: "line-through",
  under: "underline",
};

const styles: Record<TStyle, string> = {
  i: "italic",
  no: "normal",
};

const sizes: Record<TSize, string> = {
  big: "3",
  medium: "4",
  small: "6",
  xs: "7",
};

const Text = styled.p.attrs(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    size = "small",
  }: ITextProps): {
    className: string;
  } => ({
    className: `comp-text f${sizes[size]} mb${mb} ml${ml} mr${mr} mt${mt}`,
  })
)<ITextProps>`
  ${({
    bright = 1,
    decor = [],
    disp = "block",
    fontSize = "auto",
    fs = "no",
    fw = 4,
    tone = "dark",
    ta = "start",
    ws = "pre-line",
    hoverBright = bright,
    hoverTone = tone,
  }): string => `
    color: #${colors[tone][bright]};
    display: ${disp};
    font-style: ${styles[fs]};
    font-size: ${fontSize};
    font-weight: ${fw * 100};
    text-align: ${ta};
    text-decoration: ${decor.map((el): string => decors[el]).join(" ")};
    transition: all 0.3s ease;
    white-space: ${ws};
    width: ${disp === "block" ? "100%" : "auto"};
    :hover {
      color: #${colors[hoverTone][hoverBright]};
    }
  `}
`;

export type { ITextProps, TColor };
export { Text, colors };
