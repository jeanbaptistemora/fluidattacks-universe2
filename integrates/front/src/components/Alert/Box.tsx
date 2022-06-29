import styled from "styled-components";

interface IAlertBoxProps {
  variant: "error" | "info" | "success" | "warning";
}

interface IVariant {
  bgColor: string;
  color: string;
}

const variants: Record<IAlertBoxProps["variant"], IVariant> = {
  error: {
    bgColor: "#f2dede",
    color: "#a94442",
  },
  info: {
    bgColor: "#e5f6fd",
    color: "#014361",
  },
  success: {
    bgColor: "#c2ffd4",
    color: "#009245",
  },
  warning: {
    bgColor: "#fff4e5",
    color: "#663c00",
  },
};

const AlertBox = styled.div<IAlertBoxProps>`
  background-color: ${({ variant }): string => variants[variant].bgColor};
  border-radius: 4px;
  color: ${({ variant }): string => variants[variant].color};
  padding: 10px 16px;
  font-family: Roboto;
  font-size: 16px;
  margin: 10px;
  transition: all 0.3s ease;
`;

export type { IAlertBoxProps };
export { AlertBox };
