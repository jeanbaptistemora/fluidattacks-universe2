import styled from "styled-components";

import type {
  ISize,
  IStyledButtonProps,
  IVariant,
  TSize,
  TVariant,
} from "./types";

const sizes: Record<TSize, ISize> = {
  lg: {
    fontSize: 20,
    ph: 24,
    pv: 10,
  },
  md: {
    fontSize: 16,
    ph: 16,
    pv: 10,
  },
  sm: {
    fontSize: 12,
    ph: 16,
    pv: 10,
  },
};

const variants: Record<TVariant, IVariant> = {
  darkGhost: {
    bgColor: "transparent",
    bgColorHover: "#f4f4f6",
    borderColor: "transparent",
    borderRadius: 4,
    borderSize: 1,
    color: "#f4f4f6",
    colorHover: "#535365",
  },
  darkSecondary: {
    bgColor: "#535365",
    bgColorHover: "#40404f",
    borderColor: "#535365",
    borderRadius: 4,
    borderSize: 1,
    color: "#fff",
    colorHover: "#fff",
  },
  darkTertiary: {
    bgColor: "transparent",
    bgColorHover: "#f4f4f6",
    borderColor: "#f4f4f6",
    borderRadius: 4,
    borderSize: 1,
    color: "#f4f4f6",
    colorHover: "#535365",
  },
  ghost: {
    bgColor: "transparent",
    bgColorHover: "#f4f4f6",
    borderColor: "transparent",
    borderRadius: 4,
    borderSize: 1,
    color: "#535365",
    colorHover: "535365",
  },
  primary: {
    bgColor: "#bf0b1a",
    bgColorHover: "#da1e28",
    borderColor: "#bf0b1a",
    borderRadius: 4,
    borderSize: 1,
    color: "#fff",
    colorHover: "#fff",
  },
  secondary: {
    bgColor: "#2e2e38",
    bgColorHover: "#535365",
    borderColor: "#2e2e38",
    borderRadius: 4,
    borderSize: 1,
    color: "#fff",
    colorHover: "#fff",
  },
  tertiary: {
    bgColor: "transparent",
    bgColorHover: "#bf0b1a",
    borderColor: "#bf0b1a",
    borderRadius: 4,
    borderSize: 1,
    color: "#bf0b1a",
    colorHover: "#fff",
  },
};

const StyledButton = styled.button.attrs<IStyledButtonProps>(
  ({ type = "button" }): Partial<IStyledButtonProps> => ({
    type,
  })
)<IStyledButtonProps>`
  ${({
    display = "inline-block",
    selected = false,
    size = "md",
    variant = "ghost",
  }): string => {
    const { fontSize, ph, pv } = sizes[size];
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
    background-color: ${selected ? bgColorHover : bgColor};
    border: ${borderSize}px solid ${borderColor};
    border-radius: ${borderRadius}px;
    color: ${color};
    display: ${display};
    font-size: ${fontSize}px;
    font-weight: 400;
    padding: ${pv}px ${ph}px;
    text-align: start;
    text-decoration: none;
    transition: all 0.3s ease;
    width: ${display === "block" ? "100%" : "auto"};

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

export type { IStyledButtonProps, TVariant };
export { StyledButton };
