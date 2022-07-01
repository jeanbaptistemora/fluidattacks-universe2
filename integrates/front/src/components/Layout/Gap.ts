import styled from "styled-components";

interface IGapProps {
  display?: "block" | "flex" | "inline-block" | "inline";
  hg?: number;
  vg?: number;
}

const Gap = styled.div.attrs({
  className: "comp-gap",
})<IGapProps>`
  ${({ display = "flex", hg = 4, vg = 0 }): string => `
  display: ${display};
  margin: ${-vg}px ${-hg}px;

  > * {
    margin: ${vg}px ${hg}px;
  }
  `}
`;

export type { IGapProps };
export { Gap };
