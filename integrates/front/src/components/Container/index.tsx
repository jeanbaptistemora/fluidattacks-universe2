import styled from "styled-components";

type TAlign = "center" | "end" | "start" | "stretch" | "unset";
type TDisplay = "block" | "flex" | "ib" | "inline" | "none";
type TWrap = "nowrap" | "unset" | "wrap";

interface IContainerProps {
  align?: TAlign;
  bgColor?: string;
  bgImage?: string;
  bgImagePos?: string;
  borderTl?: string;
  borderTR?: string;
  borderBL?: string;
  borderBR?: string;
  display?: TDisplay;
  fontFamily?: string;
  height?: string;
  margin?: string;
  maxHeight?: string;
  maxWidth?: string;
  minHeight?: string;
  minWidth?: string;
  pb?: string;
  pl?: string;
  pr?: string;
  pt?: string;
  position?: string;
  positionBottom?: string;
  positionLeft?: string;
  positionRight?: string;
  positionTop?: string;
  scroll?: "none" | "x" | "xy" | "y";
  width?: string;
  wrap?: TWrap;
}

const Container = styled.div.attrs({
  className: "comp-container",
})<IContainerProps>`
  ${({
    align = "unset",
    bgColor = "transparent",
    bgImage = "",
    bgImagePos = "",
    borderTl = "0px 0px",
    borderTR = "0px 0px",
    borderBL = "0px 0px",
    borderBR = "0px 0px",
    display = "block",
    fontFamily = "Roboto, sans-serif",
    height = "max-content",
    margin = "0",
    maxHeight = "100%",
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    pb = "0",
    pl = "0",
    pr = "0",
    pt = "0",
    position = "static",
    positionBottom = "",
    positionLeft = "",
    positionRight = "",
    positionTop = "",
    scroll = "y",
    width = "auto",
    wrap = "unset",
  }): string => `
align-items: ${align};
background-color: ${bgColor};
background-image: ${bgImage};
background-size: ${bgImagePos};
background-repeat: no-repeat;
border-top-left-radius: ${borderTl};
border-top-right-radius: ${borderTR};
border-bottom-right-radius: ${borderBR};
border-bottom-left-radius: ${borderBL};
display: ${display};
flex-wrap: ${wrap};
font-family: ${fontFamily};
height: ${height};
margin: ${margin};
max-height: ${maxHeight};
max-width: ${maxWidth};
min-height: ${minHeight};
min-width: ${minWidth};
overflow-x: ${scroll.includes("x") ? "auto" : "hidden"};
overflow-y: ${scroll.includes("y") ? "auto" : "hidden"};
padding-bottom: ${pb};
padding-left: ${pl};
padding-right: ${pr};
padding-top: ${pt};
position: ${position};
bottom: ${positionBottom};
left: ${positionLeft};
top: ${positionTop};
right: ${positionRight};
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
