import styled from "styled-components";

interface IRowProps {
  align?: "center" | "flex-end" | "flex-start";
  justify?:
    | "center"
    | "flex-end"
    | "flex-start"
    | "space-around"
    | "space-between"
    | "space-evenly";
}

const getAlignItems = (align: IRowProps["align"]): string => {
  if (align === undefined) {
    return "flex-start";
  }

  return align;
};

const getJustifyContent = (justify: IRowProps["justify"]): string => {
  if (justify === undefined) {
    return "flex-start";
  }

  return justify;
};

const getTextAlign = (justify: IRowProps["justify"]): string => {
  if (justify === "center") {
    return "center";
  } else if (justify === "flex-end") {
    return "end";
  } else if (justify === "flex-start") {
    return "start";
  }

  return "unset";
};

const Row = styled.div.attrs({
  className: "flex flex-row flex-wrap",
})<IRowProps>`
  align-items: ${(props): string => getAlignItems(props.align)};
  justify-content: ${(props): string => getJustifyContent(props.justify)};
  text-align: ${(props): string => getTextAlign(props.justify)};
`;

export { Row };
