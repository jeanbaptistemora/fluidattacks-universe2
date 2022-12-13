import styled from "styled-components";

const StyledSelect = styled.select.attrs({
  className: `
      br2 ph2 pv2
    `,
})`
  background-color: transparent;
  border: 1px solid #b0b0bf;
  color: #2e2e38;
  outline: none;
  width: 100%;
  box-sizing: border-box;
`;

const StyledOption = styled.option.attrs({
  className: ``,
})``;

export { StyledSelect, StyledOption };
