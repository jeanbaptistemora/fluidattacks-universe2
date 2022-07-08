import styled, { css } from "styled-components";

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
    bgColor: "#fff",
  },
};

const sharedStyles = css`
  background: none;
  border: none !important;
  box-shadow: none;
  color: #121216;
  line-height: 1.25;
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
  width: 100%;

  > .comp-alert {
  ${({ showAlert }): string => `
    font-size: ${showAlert ? "14px" : "0"};
    ${showAlert ? "" : "line-height: 0;"}
    margin-top: ${showAlert ? " 6px" : "0"};
    padding: ${showAlert ? "6px 8px" : "0"};
  `}
`;

const InputWrapper = styled.div<IStyledInputProps>`
  align-items: center;
  background-color: ${({ variant }): string => variants[variant].bgColor};
  border: 1px solid #d2d2da;
  border-radius: 4px;
  color: #b0b0bf;
  display: flex;
  padding: 4px;
  transition: all 0.3s ease;
`;

const StyledInput = styled.input`
  ${sharedStyles}
`;

const StyledSelect = styled.select`
  ${sharedStyles}
`;

const StyledTextArea = styled.textarea`
  ${sharedStyles}
  resize: none;
`;

export type { IInputContainerProps, IStyledInputProps };
export { InputBox, InputWrapper, StyledInput, StyledSelect, StyledTextArea };
