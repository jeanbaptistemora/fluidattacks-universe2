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
  mh?: Nums1To7 | 0;
  mv?: Nums1To7 | 0;
  size?: Nums1To7;
  tone?: TColor;
  weight?: Nums1To9;
}

const Text = styled.p.attrs(
  ({
    mh = 0,
    mv = 0,
    size = 5,
    weight = 4,
  }: ITextProps): {
    className: string;
  } => ({
    className: `f${size} fw${weight} mh${mh} mv${mv}`,
  })
)<ITextProps>`
  ${({ bright = 1, tone = "dark" }): string => `
    color: #${colors[tone][bright]};
  `}
`;

export type { ITextProps };
export { Text, colors };
