import styled from "styled-components";

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
  className: "flex flex-row flex-wrap items-center",
})<IRowProps>`
  justify-content: ${(props): string => getJustifyContent(props.align)};
  text-align: ${(props): string => getTextAlign(props.align)};
`;

export { Row };
