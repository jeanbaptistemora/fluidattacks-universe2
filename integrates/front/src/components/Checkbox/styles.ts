import styled from "styled-components";

interface ICheckboxLabelProps {
  disabled?: boolean;
}

const CheckboxInput = styled.input.attrs({
  type: "checkbox",
})`
  display: none;
`;

const CheckboxLabel = styled.label.attrs({
  className: "comp-checkbox",
})<ICheckboxLabelProps>`
  background-color: #e9e9ed;
  border: 1px solid #c7c7d1;
  border-radius: 4px;
  color: #121216;
  display: inline-block;
  height: 18px;
  position: relative;
  transition: all 0.3s ease;
  width: 18px;

  ${({ disabled = false }): string =>
    disabled
      ? `
      cursor: not-allowed;
      opacity: 0.5;
      `
      : ""}

  :hover {
    background-color: #c7c7d1;
    border-color: #a5a5b6;
  }

  > svg {
    height: 70%;
    left: 15%;
    position: absolute;
    top: 15%;
    width: 70%;
  }
`;

export type { ICheckboxLabelProps };
export { CheckboxInput, CheckboxLabel };
