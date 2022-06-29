import styled from "styled-components";

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  margin?: string;
  padding?: string;
  variant: "basic" | "gray" | "primary" | "secondary";
}

interface IVariant {
  bgColor: string;
  bgColorHover: string;
  borderColor: string;
  color: string;
  colorHover: string;
}

const variants: Record<IButtonProps["variant"], IVariant> = {
  basic: {
    bgColor: "#dddde300",
    bgColorHover: "#dddde3",
    borderColor: "#dddde300",
    color: "#5c5c70",
    colorHover: "#121216",
  },
  gray: {
    bgColor: "#e9e9ed",
    bgColorHover: "#c7c7d1",
    borderColor: "#e9e9ed",
    color: "#5c5c70",
    colorHover: "#121216",
  },
  primary: {
    bgColor: "#ff3435",
    bgColorHover: "#b80000",
    borderColor: "#ff3435",
    color: "#fff",
    colorHover: "white",
  },
  secondary: {
    bgColor: "transparent",
    bgColorHover: "#ff3435",
    borderColor: "#ff3435",
    color: "#ff3435",
    colorHover: "white",
  },
};

const Button = styled.button.attrs<IButtonProps>(
  (props): Partial<IButtonProps> => ({
    type: props.type ?? "button",
  })
)<IButtonProps>`
  ${({ margin = "0 12px 0 0", padding = "10px 16px", variant }): string => {
    const { bgColor, bgColorHover, borderColor, color, colorHover } =
      variants[variant];

    return `
    background-color: ${bgColor};
    border: 2px solid ${borderColor};
    border-radius: 4px;
    color: ${color};
    font-weight: 400;
    margin: ${margin};
    padding: ${padding};
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
