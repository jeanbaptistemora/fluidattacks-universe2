import styled from "styled-components";

type TAlign = "center" | "end" | "start" | "stretch";
type TJustify = "around" | "between" | "center" | "end" | "evenly" | "start";

interface IRowProps {
  align?: TAlign;
  justify?: TJustify;
}

const aligns: Record<TAlign, string> = {
  center: "center",
  end: "flex-end",
  start: "flex-start",
  stretch: "stretch",
};

const justifies: Record<TJustify, string> = {
  around: "space-around",
  between: "space-between",
  center: "center",
  end: "flex-end",
  evenly: "space-evenly",
  start: "flex-start",
};

const textAligns: Record<TJustify, string> = {
  around: "unset",
  between: "unset",
  center: "center",
  end: "end",
  evenly: "unset",
  start: "start",
};

const Row = styled.div.attrs({
  className: "comp-row flex flex-row flex-wrap",
})<IRowProps>`
  ${({ align = "stretch", justify = "start" }): string => `
    align-items: ${aligns[align]};
    justify-content: ${justifies[justify]};
    text-align: ${textAligns[justify]};
  `}

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
