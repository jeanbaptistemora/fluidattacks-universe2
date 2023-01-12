import type { TSize } from "../Typography/types";

type Nums0To7 = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7;
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
  paragraph?: string;
  pv?: Nums0To7;
  image?: string;
  matomoAction: string;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
  variant?: TVariant;
}

export type { ICtaBannerProps, IVariant, TVariant };
