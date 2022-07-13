import styled from "styled-components";

interface IRowProps {
  align?: "center" | "flex-end" | "flex-start" | "stretch";
  justify?:
    | "center"
    | "flex-end"
    | "flex-start"
    | "space-around"
    | "space-between"
    | "space-evenly";
}

const getAlignItems = (align: IRowProps["align"]): string => align ?? "stretch";

const getJustifyContent = (justify: IRowProps["justify"]): string =>
  justify ?? "flex-start";

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
  className: "comp-row flex flex-row flex-wrap",
})<IRowProps>`
  align-items: ${({ align }): string => getAlignItems(align)};
  justify-content: ${({ justify }): string => getJustifyContent(justify)};
  text-align: ${({ justify }): string => getTextAlign(justify)};

  margin: -6px;

  > *:not(.comp-col) {
    width: 100%;
    margin: 6px;
  }

  > .comp-col {
    padding: 6px;
  }
`;

export { Row };
