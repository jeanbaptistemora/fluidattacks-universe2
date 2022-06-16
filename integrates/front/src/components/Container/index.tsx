import styled from "styled-components";

interface IContainerProps {
  height?: string;
  margin?: string;
  maxHeight?: string;
  maxWidth?: string;
  minHeight?: string;
  minWidth?: string;
  padding?: string;
  scroll?: "none" | "x" | "xy" | "y";
  width?: string;
}

const Container = styled.div.attrs({
  className: "comp-container",
})<IContainerProps>`
  ${({
    height = "100%",
    margin = "0",
    maxHeight = "100%",
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    padding = "0",
    scroll = "y",
    width = "100%",
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
