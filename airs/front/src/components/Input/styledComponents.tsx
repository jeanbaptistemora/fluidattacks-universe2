import styled from "styled-components";

import type { IStyledInputProps } from "./types";

const StyledInput = styled.input.attrs({
  className: `
      br2 ph2
    `,
})<IStyledInputProps>`
  ${({ bgColor = "transparent", borderColor = "#b0b0bf" }): string => {
    return `
      background-color: ${bgColor};
      border: 1px solid ${borderColor};
      box-sizing: border-box;
      color: #2e2e38;
      outline: none;
      padding-top: 0.6rem;
      padding-bottom: 0.6rem;
      width: 100%;
    `;
  }}
`;

export { StyledInput };
