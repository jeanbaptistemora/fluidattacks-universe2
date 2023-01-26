import styled, { css } from "styled-components";

type TInputVariant = "outline" | "solid";

interface IInputContainerProps {
  showAlert: boolean;
}

interface IStyledInputProps {
  variant?: TInputVariant;
}

interface IVariant {
  bgColor: string;
}

const variants: Record<TInputVariant, IVariant> = {
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
  box-sizing: border-box;
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

const InputBox = styled.div<IInputContainerProps>`
  width: 100%;

  > .comp-alert {
    font-size: 14px;
    margin-top: ${({ showAlert }): number => (showAlert ? 4 : 0)}px;
  }
`;

const InputWrapper = styled.div<IStyledInputProps>`
  ${({ variant = "solid" }): string => `
  align-items: center;
  background-color: ${variants[variant].bgColor};
  border: 1px solid #d2d2da;
  border-radius: 4px;
  color: #b0b0bf;
  display: flex;
  padding: 4px;
  transition: all 0.3s ease;
  `}
`;

const StyledInput = styled.input`
  ${sharedStyles}
  ::-webkit-outer-spin-button,
  ::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
  }

  &[type="number"] {
    -moz-appearance: textfield;
  }
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
