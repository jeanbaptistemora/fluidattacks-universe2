import styled from "styled-components";

interface IStyledInputProps {
  disabled?: boolean;
  id?: string;
  placeholder?: string;
  type?: "email" | "password" | "text";
  variant: "outline" | "solid";
}

interface IStyledInputAlertProps {
  show: boolean;
}

interface IVariant {
  bgColor: string;
}

const variants: Record<IStyledInputProps["variant"], IVariant> = {
  outline: {
    bgColor: "transparent",
  },
  solid: {
    bgColor: "#e9e9ed",
  },
};

const StyledInput = styled.input<IStyledInputProps>`
  background-color: ${(props): string => variants[props.variant].bgColor};
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

const Alert = styled.p<IStyledInputAlertProps>`
  background-color: #feeced;
  border-radius: 4px;
  color: #3a0306;
  font-size: 12px;
  font-weight: 500;
  height: ${(props): number => (props.show ? 25 : 0)}px;
  line-height: ${(props): number => (props.show ? 25 : 0)}px;
  margin-bottom: 0;
  margin-top: 6px;
  padding: 0 0.5rem;
  transition: all 0.3s ease;
`;

const Container = styled.div`
  font-family: "Roboto", sans-serif;
  max-width: 350px;
`;

export type { IStyledInputProps };
export { Alert, Container, StyledInput };
