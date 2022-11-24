import type { ButtonHTMLAttributes } from "react";

type TDisplay = "block" | "inline-block" | "inline";
type TSize = "lg" | "md" | "sm";
type TVariant =
  | "darkGhost"
  | "darkSecondary"
  | "darkTertiary"
  | "ghost"
  | "primary"
  | "secondary"
  | "tertiary";

interface IStyledButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  display?: TDisplay;
  size?: TSize;
  variant?: TVariant;
}

interface ISize {
  fontSize: number;
  ph: number;
  pv: number;
}

interface IVariant {
  bgColor: string;
  bgColorHover: string;
  borderColor: string;
  borderRadius: number;
  borderSize: number;
  color: string;
  colorHover: string;
}

export type { ISize, IStyledButtonProps, IVariant, TDisplay, TSize, TVariant };
