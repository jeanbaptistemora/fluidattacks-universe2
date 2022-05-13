import styled from "styled-components";

interface IBoxProps {
  variant: "error" | "info" | "success" | "warning";
}

interface IVariant {
  backgroundColor: string;
  color: string;
}

const variants: Record<IBoxProps["variant"], IVariant> = {
  error: {
    backgroundColor: "#f2dede",
    color: "#a94442",
  },
  info: {
    backgroundColor: "#e5f6fd",
    color: "#014361",
  },
  success: {
    backgroundColor: "#c2ffd4",
    color: "#009245",
  },
  warning: {
    backgroundColor: "#fff4e5",
    color: "#663c00",
  },
};

const Box = styled.div<IBoxProps>`
  background-color: ${(props): string =>
    variants[props.variant].backgroundColor};
  border-radius: 4px;
  color: ${(props): string => variants[props.variant].color};
  padding: 0px 20px 10px 20px;
  font-family: Roboto;
  font-size: 16px;
`;

export type { IBoxProps };
export { Box };
