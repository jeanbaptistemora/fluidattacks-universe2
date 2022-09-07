/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

type TAlign = "center" | "end" | "start" | "stretch";
type TJustify = "around" | "between" | "center" | "end" | "evenly" | "start";

interface IRowProps {
  align?: TAlign;
  cols?: number;
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

/**
 * @param cols Total of cols for this Row's descendants
 */
const Row = styled.div.attrs({
  className: "comp-row flex flex-row flex-wrap",
})<IRowProps>`
  ${({ align = "stretch", cols = 100, justify = "start" }): string => `
  align-items: ${aligns[align]};
  justify-content: ${justifies[justify]};
  margin: -6px;
  text-align: ${textAligns[justify]};

  --cols: ${cols};

  > *:not(.comp-col) {
    width: 100%;
    margin: 6px;
  }

  > .comp-col {
    padding: 6px;
  }
  `}
`;

export { Row };
