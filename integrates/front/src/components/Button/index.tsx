import styled from "styled-components";

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant: "basic" | "gray" | "primary" | "secondary";
}

interface IVariant {
  backgroundColor: string;
  borderColor: string;
  color: string;
  hoverBackgroundColor: string;
  hoverColor: string;
}

const variants: Record<IButtonProps["variant"], IVariant> = {
  basic: {
    backgroundColor: "transparent",
    borderColor: "transparent",
    color: "#5c5c70",
    hoverBackgroundColor: "transparent",
    hoverColor: "black",
  },
  gray: {
    backgroundColor: "#e9e9ed",
    borderColor: "#e9e9ed",
    color: "#5c5c70",
    hoverBackgroundColor: "#e9e9ed",
    hoverColor: "#5c5c70",
  },
  primary: {
    backgroundColor: "#ff3435",
    borderColor: "#ff3435",
    color: "#fff",
    hoverBackgroundColor: "#b80000",
    hoverColor: "white",
  },
  secondary: {
    backgroundColor: "transparent",
    borderColor: "#ff3435",
    color: "#ff3435",
    hoverBackgroundColor: "#ff3435",
    hoverColor: "white",
  },
};

const Button = styled.button.attrs<IButtonProps>(
  (props): Partial<IButtonProps> => ({
    type: props.type ?? "button",
  })
)<IButtonProps>`
  background-color: ${(props): string =>
    variants[props.variant].backgroundColor};
  border-color: ${(props): string => variants[props.variant].borderColor};
  border-radius: 4px;
  border-style: solid;
  border-width: 2px;
  color: ${(props): string => variants[props.variant].color};
  font-weight: 400;
  padding: 10px 16px;
  text-decoration: none;
  transition: all 0.3s ease;

  :disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
  :hover:not([disabled]) {
    background-color: ${(props): string =>
      variants[props.variant].hoverBackgroundColor};
    border-color: ${(props): string =>
      variants[props.variant].hoverBackgroundColor};
    color: ${(props): string => variants[props.variant].hoverColor};
    cursor: pointer;
  }
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
