/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ButtonHTMLAttributes } from "react";
import styled from "styled-components";

type TSize = "lg" | "md" | "sm" | "xl" | "xs";
type TVariant =
  | "ghost"
  | "input"
  | "primary"
  | "secondary"
  | "selected-input"
  | "tertiary";

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

const sizes: Record<TSize, ISize> = {
  lg: {
    fontSize: 5,
    ph: 18,
    pv: 12,
  },
  md: {
    fontSize: 6,
    ph: 15,
    pv: 10,
  },
  sm: {
    fontSize: 7,
    ph: 12,
    pv: 8,
  },
  xl: {
    fontSize: 4,
    ph: 21,
    pv: 14,
  },
  xs: {
    fontSize: 7,
    ph: 9,
    pv: 6,
  },
};

const variants: Record<TVariant, IVariant> = {
  ghost: {
    bgColor: "#80808000",
    bgColorHover: "#80808040",
    borderColor: "#80808000",
    borderRadius: 4,
    borderSize: 2,
    color: "inherit",
    colorHover: "inherit",
  },
  input: {
    bgColor: "transparent",
    bgColorHover: "#d2d2da",
    borderColor: "#d2d2da",
    borderRadius: 0,
    borderSize: 1,
    color: "#121216",
    colorHover: "#fff",
  },
  primary: {
    bgColor: "#bf0b1a",
    bgColorHover: "#f2182a",
    borderColor: "#bf0b1a",
    borderRadius: 4,
    borderSize: 2,
    color: "#fff",
    colorHover: "#fff",
  },
  secondary: {
    bgColor: "#2e2e38",
    bgColorHover: "#49495a",
    borderColor: "#2e2e38",
    borderRadius: 4,
    borderSize: 2,
    color: "#d2d2da",
    colorHover: "#f4f4f6",
  },
  "selected-input": {
    bgColor: "#e9e9ed",
    bgColorHover: "#d2d2da",
    borderColor: "#2e2e38",
    borderRadius: 0,
    borderSize: 1,
    color: "#121216",
    colorHover: "#fff",
  },
  tertiary: {
    bgColor: "transparent",
    bgColorHover: "#bf0b1a",
    borderColor: "#bf0b1a",
    borderRadius: 4,
    borderSize: 2,
    color: "#bf0b1a",
    colorHover: "#fff",
  },
};

const StyledButton = styled.button.attrs<IStyledButtonProps>(
  ({ size = "md", type = "button" }): Partial<IStyledButtonProps> => ({
    className: `comp-button f${sizes[size].fontSize}`,
    type,
  })
)<IStyledButtonProps>`
  ${({ disp = "inline-block", size = "md", variant = "ghost" }): string => {
    const { ph, pv } = sizes[size];
    const {
      bgColor,
      bgColorHover,
      borderColor,
      borderRadius,
      borderSize,
      color,
      colorHover,
    } = variants[variant];

    return `
    background-color: ${bgColor};
    border: ${borderSize}px solid ${borderColor};
    border-radius: ${borderRadius}px;
    color: ${color};
    display: ${disp};
    font-weight: 400;
    padding: ${pv}px ${ph}px;
    text-align: start;
    text-decoration: none;
    transition: all 0.3s ease;
    width: ${disp === "block" ? "100%" : "auto"};

    :disabled {
      cursor: not-allowed;
      opacity: 0.5;
    }
    :hover:not([disabled]) {
      background-color: ${bgColorHover};
      border-color: ${bgColorHover};
      color: ${colorHover};
      cursor: pointer;
    }
    `;
  }}
`;

export type { IStyledButtonProps };
export { StyledButton };
