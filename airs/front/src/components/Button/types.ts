/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ButtonHTMLAttributes } from "react";

type TSize = "lg" | "md" | "sm";
type TVariant = "ghost" | "primary" | "secondary" | "tertiary";

interface IStyledButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  disp?: "block" | "inline-block" | "inline";
  selected?: boolean;
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

export type { ISize, IStyledButtonProps, IVariant, TSize, TVariant };
