import styled from "styled-components";

interface IAlertBoxProps {
  show?: boolean;
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

const AlertBox = styled.div.attrs({
  className: "comp-alert",
})<IAlertBoxProps>`
  align-items: center;
  border-radius: 4px;
  display: flex;
  font-size: 16px;
  justify-content: space-between;
  overflow: hidden;
  transition: all 0.3s ease;

  ${({ show = true, variant }): string => `
    background-color: ${variants[variant].bgColor};
    color: ${variants[variant].color};
    height: ${show ? 35 : 0}px;
    padding: ${show ? "10px 16px" : 0};
  `}

  > .comp-button {
    background-color: transparent !important;
    border: none !important;
    margin-right: -10px;
    padding: 4px 8px;
  }
`;

export type { IAlertBoxProps };
export { AlertBox };
