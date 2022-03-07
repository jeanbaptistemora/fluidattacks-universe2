import styled, { css } from "styled-components";

import { IntlTelInputWrapper } from "components/IntlTelInputWrapper";

const baseInputStyles = css`
  font-size: 16px;

  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;
const baseInputClassName = "w-100 pa2 lh-copy gray bw1 b--light-gray b--solid";

const StyledInput = styled.input.attrs<{ className: string }>({
  className: baseInputClassName,
})`
  ${baseInputStyles}
`;

const StyledPhoneNumberInput = styled(IntlTelInputWrapper).attrs<{
  className: string;
}>({
  className: baseInputClassName,
})`
  ${baseInputStyles}
`;

const StyledSelect = styled.select.attrs({
  className: "w-100 pa2 lh-copy gray bw1 b--light-gray",
})`
  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;

const ValidationError = styled.div.attrs({
  className: "dark-red",
})``;

export { StyledPhoneNumberInput, StyledInput, StyledSelect, ValidationError };
