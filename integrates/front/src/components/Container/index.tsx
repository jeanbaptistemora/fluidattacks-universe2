/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

interface IContainerProps {
  height?: string;
  margin?: string;
  maxHeight?: string;
  maxWidth?: string;
  minHeight?: string;
  minWidth?: string;
  padding?: string;
  pb?: string;
  pl?: string;
  pr?: string;
  pt?: string;
  scroll?: "none" | "x" | "xy" | "y";
  width?: string;
}

const Container = styled.div.attrs({
  className: "comp-container",
})<IContainerProps>`
  ${({
    height = "max-content",
    margin = "0",
    maxHeight = "100%",
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    padding = "0",
    pb = "0",
    pl = "0",
    pr = "0",
    pt = "0",
    scroll = "y",
    width = "auto",
  }): string => `
height: ${height};
margin: ${margin};
max-height: ${maxHeight};
max-width: ${maxWidth};
min-height: ${minHeight};
min-width: ${minWidth};
overflow-x: ${scroll.includes("x") ? "auto" : "hidden"};
overflow-y: ${scroll.includes("y") ? "auto" : "hidden"};
padding: ${padding};
padding-bottom: ${pb};
padding-left: ${pl};
padding-right: ${pr};
padding-top: ${pt};
transition: all 0.3s ease;
width: ${width};

::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #b0b0bf;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb {
  background: #65657b;
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #535365;
}`}
`;

export type { IContainerProps };
export { Container };
