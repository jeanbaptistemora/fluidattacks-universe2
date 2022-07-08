import styled from "styled-components";

/**
 * Inspired by tachyons widths
 * @link http://tachyons.io/docs/layout/widths/
 */
type Width =
  | "10"
  | "20"
  | "25"
  | "30"
  | "33"
  | "34"
  | "40"
  | "50"
  | "60"
  | "70"
  | "75"
  | "80"
  | "90"
  | "100";

interface IColProps {
  large?: Width;
  medium?: Width;
  small?: Width;
}

const getAttrs = (width?: Width): string => `
  flex-grow: ${width === undefined ? "1" : "unset"};
  width: ${width === undefined ? "unset" : `${width}%`};
`;

const Col = styled.div.attrs({
  className: "comp-col",
})<IColProps>`
  word-break: break-word;

  @media (max-width: 768px) {
    ${({ small }): string => getAttrs(small)}
  }

  @media (min-width: 768px) and (max-width: 992px) {
    ${({ medium }): string => getAttrs(medium)}
  }

  @media (min-width: 992px) {
    ${({ large }): string => getAttrs(large)}
  }
`;

export { Col };
