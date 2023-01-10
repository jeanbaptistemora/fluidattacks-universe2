import styled from "styled-components";

type TAlign = "center" | "end" | "start" | "stretch" | "unset";
type TDisplay = "block" | "flex" | "ib" | "inline" | "none";
type TWrap = "nowrap" | "unset" | "wrap";

interface IContainerProps {
  align?: TAlign;
  bgColor?: string;
  bgImage?: string;
  bgImagePos?: string;
  borderBottom?: string;
  borderTl?: string;
  borderTop?: string;
  borderTR?: string;
  borderBL?: string;
  borderBR?: string;
  border?: string;
  boxShadow?: string;
  boxSizing?: string;
  br?: string;
  display?: TDisplay;
  fontFamily?: string;
  height?: string;
  heightMd?: string;
  justify?: string;
  letterSpacing?: string;
  lineHeight?: string;
  margin?: string;
  maxHeight?: string;
  maxWidth?: string;
  minHeight?: string;
  minWidth?: string;
  pb?: string;
  pl?: string;
  pr?: string;
  pt?: string;
  pbMd?: string;
  ptMd?: string;
  prMd?: string;
  plMd?: string;
  position?: string;
  positionBottom?: string;
  positionLeft?: string;
  positionRight?: string;
  positionTop?: string;
  scroll?: "none" | "x" | "xy" | "y";
  scrollInvisible?: boolean;
  textAlign?: string;
  width?: string;
  widthMd?: string;
  wrap?: TWrap;
  zIndex?: string;
}

const Container = styled.div.attrs({
  className: "comp-container",
})<IContainerProps>`
  ${({
    align = "unset",
    bgColor = "transparent",
    bgImage = "",
    bgImagePos = "",
    borderBottom = "",
    borderTl = "0px 0px",
    borderTop = "",
    borderTR = "0px 0px",
    borderBL = "0px 0px",
    borderBR = "0px 0px",
    border = "",
    boxShadow = "",
    boxSizing = "",
    br = "0",
    display = "block",
    fontFamily = "Roboto, sans-serif",
    height = "max-content",
    heightMd = "auto",
    justify = "",
    letterSpacing = "",
    lineHeight = "normal",
    margin = "0",
    maxHeight = "100%",
    maxWidth = "100%",
    minHeight = "0",
    minWidth = "0",
    pb = "0",
    pl = "0",
    pr = "0",
    pt = "0",
    pbMd = "0",
    ptMd = "0",
    prMd = "0",
    plMd = "0",
    position = "static",
    positionBottom = "",
    positionLeft = "",
    positionRight = "",
    positionTop = "",
    scroll = "y",
    scrollInvisible = false,
    textAlign = "",
    width = "auto",
    widthMd = "auto",
    wrap = "unset",
    zIndex = "auto",
  }): string => `
align-items: ${align};
background-color: ${bgColor};
background-image: ${bgImage};
background-size: ${bgImagePos};
background-repeat: no-repeat;
border: ${border};
border-bottom: ${borderBottom};
border-top: ${borderTop};
border-top-left-radius: ${borderTl};
border-top-right-radius: ${borderTR};
border-bottom-right-radius: ${borderBR};
border-bottom-left-radius: ${borderBL};
border-radius: ${br};
box-shadow: ${boxShadow};
box-sizing: ${boxSizing};
display: ${display};
flex-wrap: ${wrap};
font-family: ${fontFamily};
height: ${height};
justify-content: ${justify};
letter-spacing: ${letterSpacing};
line-height: ${lineHeight};
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
text-align: ${textAlign};
transition: all 0.3s ease;
width: ${width};
z-index: ${zIndex};

@media screen and (min-width: 64em) {
   width: ${width};
    }

@media screen and (max-width: 64em), (max-height: 40em) {
  box-sizing: ${boxSizing};
   width: ${widthMd === "auto" ? width : widthMd};
   padding-bottom: ${pbMd === "0" ? pb : pbMd};
   padding-top: ${ptMd === "0" ? pt : ptMd};
   padding-left: ${plMd === "0" ? pl : plMd};
   padding-right: ${prMd === "0" ? pr : prMd};
   height: ${heightMd === "auto" ? height : heightMd};
    }

::-webkit-scrollbar {
  width: ${scrollInvisible ? "0px" : "8px"};
}
::-webkit-scrollbar-track {
  background: #b0b0bf;
  opacity: ${scrollInvisible ? "0" : "1"};
  border-radius: 4px;
}
::-webkit-scrollbar-thumb {
  background: #65657b;
  opacity: ${scrollInvisible ? "0" : "1"};
  border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
  background: #535365;
  opacity: ${scrollInvisible ? "0" : "1"};
}`}
`;

export type { IContainerProps };
export { Container };
