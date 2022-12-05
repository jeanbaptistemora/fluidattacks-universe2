import type { TDisplay, TVariant } from "../Button/types";

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
