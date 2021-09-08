import styled from "styled-components";

const StyledInput = styled.input.attrs({
  className: "w-100 pa2 lh-copy gray bw1 b--light-gray b--solid",
})`
  font-size: 16px;

  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;

const StyledSelect = styled.select.attrs({
  className: "w-100 pa2 lh-copy gray bg-white bw1 b--light-gray",
})`
  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;

const ValidationError = styled.div.attrs({
  className: "dark-red",
})``;

export { StyledInput, StyledSelect, ValidationError };
