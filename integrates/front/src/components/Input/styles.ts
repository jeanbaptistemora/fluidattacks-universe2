import styled from "styled-components";

interface IInputContainerProps {
  showAlert: boolean;
}

interface IStyledInputProps {
  variant: "outline" | "solid";
}

interface IVariant {
  bgColor: string;
}

const variants: Record<IStyledInputProps["variant"], IVariant> = {
  outline: {
    bgColor: "transparent",
  },
  solid: {
    bgColor: "#f4f4f6",
  },
};

const StyledInput = styled.input`
  background: none;
  border: none;
  color: #121216;
  font-weight: 400;
  outline: none;
  padding: 6px 12px;
  width: 100%;

  :disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }
  ::placeholder {
    color: #b0b0bf;
  }
`;

const InputBox = styled.div.attrs({
  className: "comp-input",
})<IInputContainerProps>`
  font-family: Roboto, sans-serif;
  max-width: 400px;
  width: 100%;

  > .comp-alert {
  ${({ showAlert }): string => `
    font-size: ${showAlert ? "14px" : "0"};
    ${showAlert ? "" : "line-height: 0;"}
    margin: ${showAlert ? " 6px 0 0 0" : "0"};
    padding: ${showAlert ? "6px 8px" : "0"};
  `}
`;

const InputWrapper = styled.div<IStyledInputProps>`
  align-items: center;
  background-color: ${({ variant }): string => variants[variant].bgColor};
  border: 1px solid #b0b0bf;
  border-radius: 4px;
  color: #b0b0bf;
  display: flex;
  padding: 4px;
  transition: all 0.3s ease;
`;

export type { IInputContainerProps, IStyledInputProps };
export { InputBox, InputWrapper, StyledInput };
