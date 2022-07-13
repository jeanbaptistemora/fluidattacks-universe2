import styled from "styled-components";

interface IHrProps {
  mv?: 8 | 16 | 24 | 32;
}

const Hr = styled.hr.attrs({
  className: "comp-hr",
})<IHrProps>`
  background-color: #dddde3;
  height: 1px;
  margin: ${({ mv = 8 }): number => mv}px 0;
  width: 100%;
`;

export type { IHrProps };
export { Hr };
