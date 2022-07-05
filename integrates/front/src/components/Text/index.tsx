import styled from "styled-components";

type TColor = "dark" | "light" | "red";
type Nums1To7 = 1 | 2 | 3 | 4 | 5 | 6 | 7;
type Nums1To9 = Nums1To7 | 8 | 9;

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
    "ddde3",
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

interface ITextProps {
  bright?: Nums1To9 | 0;
  hoverBright?: Nums1To9 | 0;
  hoverTone?: TColor;
  mb?: Nums1To7 | 0;
  ml?: Nums1To7 | 0;
  mr?: Nums1To7 | 0;
  mt?: Nums1To7 | 0;
  size?: Nums1To7;
  tone?: TColor;
  fw?: Nums1To9;
}

const Text = styled.p.attrs(
  ({
    mb = 0,
    ml = 0,
    mr = 0,
    mt = 0,
    size = 3,
    fw = 4,
  }: ITextProps): {
    className: string;
  } => ({
    className: `comp-text f${8 - size} fw${fw} mb${mb} ml${ml} mr${mr} mt${mt}`,
  })
)<ITextProps>`
  ${({
    bright = 1,
    hoverBright = 1,
    hoverTone = "dark",
    tone = "dark",
  }): string => `
    color: #${colors[tone][bright]};
    transition: all 0.3s ease;

    :hover {
      color: #${colors[hoverTone][hoverBright]};
    }
  `}
`;

export type { ITextProps };
export { Text, colors };
