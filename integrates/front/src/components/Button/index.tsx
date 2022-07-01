import styled from "styled-components";

type TSize = "lg" | "md" | "sm" | "xl";
type TVariant = "ghost" | "primary" | "secondary" | "tertiary";

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
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
};

const variants: Record<TVariant, IVariant> = {
  ghost: {
    bgColor: "#dddde300",
    bgColorHover: "#dddde3",
    borderColor: "#dddde300",
    color: "#5c5c70",
    colorHover: "#121216",
  },
  primary: {
    bgColor: "#bf0b1a",
    bgColorHover: "#f2182a",
    borderColor: "#bf0b1a",
    color: "#fff",
    colorHover: "white",
  },
  secondary: {
    bgColor: "#2e2e38",
    bgColorHover: "#49495a",
    borderColor: "#2e2e38",
    color: "#d2d2da",
    colorHover: "#f4f4f6",
  },
  tertiary: {
    bgColor: "transparent",
    bgColorHover: "#ff3435",
    borderColor: "#ff3435",
    color: "#ff3435",
    colorHover: "white",
  },
};

const Button = styled.button.attrs<IButtonProps>(
  ({ size = "md", type = "button" }): Partial<IButtonProps> => ({
    className: `comp-button f${sizes[size].fontSize}`,
    type,
  })
)<IButtonProps>`
  ${({ size = "md", variant = "ghost" }): string => {
    const { ph, pv } = sizes[size];
    const { bgColor, bgColorHover, borderColor, color, colorHover } =
      variants[variant];

    return `
    background-color: ${bgColor};
    border: 2px solid ${borderColor};
    border-radius: 4px;
    color: ${color};
    font-weight: 400;
    padding: ${pv}px ${ph}px;
    text-decoration: none;
    transition: all 0.3s ease;

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

const ButtonOpacity = styled.button.attrs({
  className: "bn mh1 pa2",
})`
  background: none;

  :hover {
    opacity: 0.75;
  }
`;

export type { IButtonProps };
export { Button, ButtonOpacity };
