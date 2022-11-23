import styled, { css } from "styled-components";

import { PhoneInputWrapper } from "components/PhoneInputWrapper";

const baseInputStyles = css`
  color: #777;
  width: 100% !important;
  font-size: 16px !important;
  border-style: solid !important;
  border-width: 0.125rem !important;
  border-radius: 0 !important;
  border-color: #eee !important;
  line-height: 1.5 !important;
  padding: 0.5rem;
  padding-top: 0.5rem !important;
  padding-bottom: 0.5rem !important;

  &:focus {
    border-color: #d1d1d1 !important;
    box-shadow: none !important;
    outline: none;
  }
  &:disabled {
    background: none !important;
  }
`;

const StyledInput = styled.input`
  ${baseInputStyles}
`;

const StyledPhoneInput = styled(PhoneInputWrapper)`
  ${baseInputStyles}
`;

const StyledSelect = styled.select`
  ${baseInputStyles}
`;

const ValidationError = styled.div.attrs({
  className: "dark-red",
})``;

export { StyledPhoneInput, StyledInput, StyledSelect, ValidationError };
