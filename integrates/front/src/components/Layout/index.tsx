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

const getFlexGrow = (width?: Width): string => {
  if (width === undefined) {
    return "1";
  }

  return "unset";
};

const getWidth = (width?: Width): string => {
  if (width === undefined) {
    return "unset";
  }

  return `${width}%`;
};

const Col = styled.div.attrs({ className: "pa2" })<IColProps>`
  @media (max-width: 768px) {
    flex-grow: ${(props): string => getFlexGrow(props.small)};
    width: ${(props): string => getWidth(props.small)};
  }

  @media (min-width: 768px) and (max-width: 992px) {
    flex-grow: ${(props): string => getFlexGrow(props.medium)};
    width: ${(props): string => getWidth(props.medium)};
  }

  @media (min-width: 992px) {
    flex-grow: ${(props): string => getFlexGrow(props.large)};
    width: ${(props): string => getWidth(props.large)};
  }
`;

interface IRowProps {
  align?:
    | "center"
    | "flex-end"
    | "flex-start"
    | "space-around"
    | "space-between"
    | "space-evenly";
}

const getJustifyContent = (align: IRowProps["align"]): string => {
  if (align === undefined) {
    return "flex-start";
  }

  return align;
};

const getTextAlign = (align: IRowProps["align"]): string => {
  if (align === "center") {
    return "center";
  } else if (align === "flex-end") {
    return "end";
  } else if (align === "flex-start") {
    return "start";
  }

  return "unset";
};

const Row = styled.div.attrs({
  className: "flex flex-row flex-wrap",
})<IRowProps>`
  justify-content: ${(props): string => getJustifyContent(props.align)};
  text-align: ${(props): string => getTextAlign(props.align)};
`;

export { Col, Row };
