import type { TSize } from "../Typography/types";

type TVariant = "dark" | "light";

interface IVariant {
  bgColor: string;
  color: string;
  subColor: string;
}

interface ICtaBannerProps {
  button1Link: string;
  button1Text: string;
  button2Link?: string;
  button2Text?: string;
  textSize?: TSize;
  title: string;
  paragraph: string;
  image?: string;
  matomoAction: string;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
  variant?: TVariant;
}

export type { ICtaBannerProps, IVariant, TVariant };
