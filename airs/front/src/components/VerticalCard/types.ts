import type { TDisplay, TVariant } from "../Button/types";

type Nums0To7 = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;

interface IVerticalCard {
  alt: string;
  author?: string;
  bgColor?: string;
  btnDisplay?: TDisplay;
  btnText: string;
  btnVariant?: TVariant;
  date?: string;
  description: string;
  image: string;
  imagePadding?: boolean;
  link: string;
  subMinHeight?: string;
  titleMinHeight?: string;
  mh?: Nums0To7;
  minWidth?: string;
  minWidthMd?: string;
  minWidthSm?: string;
  subtitle?: string;
  title: string;
  width?: string;
  widthMd?: string;
  widthSm?: string;
}

export type { IVerticalCard };
