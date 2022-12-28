type TVariant = "dark" | "light";

interface IVariant {
  bgColor: string;
  button: "darkSecondary" | "secondary";
  subtitleColor: string;
  titleColor: string;
}

interface ICardSlideShowProps {
  btnText: string;
  containerDescription: string;
  containerTitle: string;
  data: INodes[];
  variant?: TVariant;
}

export type { ICardSlideShowProps, IVariant, TVariant };
