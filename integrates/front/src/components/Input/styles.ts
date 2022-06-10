import styled from "styled-components";

interface IAlertProps {
  show: boolean;
  variant: "high" | "low";
}

interface IAlertVariant {
  bgColor: string;
  paddingX: number;
}

interface IStyledInputProps {
  disabled?: boolean;
  id?: string;
  placeholder?: string;
  type?: "email" | "password" | "text";
  variant: "outline" | "solid";
}

interface IVariant {
  bgColor: string;
}

const alertVariants: Record<IAlertProps["variant"], IAlertVariant> = {
  high: {
    bgColor: "#fdd8da",
    paddingX: 8,
  },
  low: {
    bgColor: "transparent",
    paddingX: 0,
  },
};

const variants: Record<IStyledInputProps["variant"], IVariant> = {
  outline: {
    bgColor: "transparent",
  },
  solid: {
    bgColor: "#e9e9ed",
  },
};

const StyledInput = styled.input<IStyledInputProps>`
  background-color: ${({ variant }): string => variants[variant].bgColor};
  border-radius: 4px;
  border: 1px solid #b0b0bf;
  box-sizing: border-box;
  color: #000;
  font-weight: 400;
  outline: none;
  padding: 10px 16px;
  transition: all 0.3s ease;
  width: 100%;

  :disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
  ::placeholder {
    color: #b0b0bf;
  }
`;

const Alert = styled.p<IAlertProps>`
  background-color: ${({ variant }): string => alertVariants[variant].bgColor};
  border-radius: 4px;
  color: #f2182a;
  font-size: 12px;
  font-weight: 500;
  height: ${({ show }): number => (show ? 25 : 0)}px;
  line-height: ${({ show }): number => (show ? 25 : 0)}px;
  margin-bottom: 0;
  margin-top: 6px;
  overflow: hidden;
  padding: 0 ${({ variant }): number => alertVariants[variant].paddingX}px;
  transition: all 0.3s ease;
`;

const Container = styled.div`
  font-family: "Roboto", sans-serif;
  max-width: 350px;
`;

export type { IAlertProps, IStyledInputProps };
export { Alert, Container, StyledInput };
