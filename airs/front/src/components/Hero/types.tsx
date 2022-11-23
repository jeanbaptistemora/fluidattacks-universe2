import type { TSize } from "../Typography/types";

interface IHeroProps {
  bgColor: string;
  button1Link: string;
  button1Text: string;
  button2Link: string;
  button2Text: string;
  title: string;
  paragraph: string;
  image: string;
  matomoAction: string;
  size?: TSize;
  sizeMd?: TSize;
  sizeSm?: TSize;
}

export type { IHeroProps };
