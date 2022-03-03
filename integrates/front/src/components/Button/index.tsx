import styled from "styled-components";

interface IButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant: "primary" | "secondary";
}

interface IVariant {
  backgroundColor: string;
  color: string;
  hoverBackgroundColor: string;
}

const variants: Record<IButtonProps["variant"], IVariant> = {
  primary: {
    backgroundColor: "#ff3435",
    color: "#fff",
    hoverBackgroundColor: "#b80000",
  },
  secondary: {
    backgroundColor: "transparent",
    color: "#ff3435",
    hoverBackgroundColor: "#ff3435",
  },
};

const Button = styled.button.attrs<IButtonProps>(
  (props): Partial<IButtonProps> => ({
    type: props.type ?? "button",
  })
)<IButtonProps>`
  background-color: ${(props): string =>
    variants[props.variant].backgroundColor};
  border-color: #ff3435;
  border-radius: 4px;
  border-style: solid;
  border-width: 2px;
  color: ${(props): string => variants[props.variant].color};
  font-weight: 400;
  margin-left: 12px;
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
    color: white;
    cursor: pointer;
  }
`;

export { Button, IButtonProps };
