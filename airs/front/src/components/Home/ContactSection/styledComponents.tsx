import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const BlueBackground: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  bg-darker-blue
  ba
  bw2
  bc-darker-blue
`,
})``;
const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  h-400
  mw-1366
  center
  ph-body
  pv5
  bg-darker-blue
`,
})``;

const Title: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
  tl
  roboto
  c-black-gray
  fw4
  f5
  mh0
`,
})``;

const MainText: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
  neue
  f3
  tl
  fw7
  c-fluid-gray
`,
})``;

const InnerSection: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  w5-l
  mv5
`,
})``;

const RedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
  roboto
  w-auto-l
  w-100
  outline-transparent
  bg-button-red
  hv-bg-fluid-rd
  pointer
  white
  pv3
  ph5
  fw4
  f5
  dib
  t-all-3-eio
  br2
  bc-fluid-red
  ba
`,
})``;

const SocialContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  flex
  mt4
  pt3
`,
})``;

const SocialButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
  pa2
  ba
  br3
  bc-gray-64
  bg-transparent
  pointer
`,
})``;

export {
  BlueBackground,
  Container,
  InnerSection,
  MainText,
  RedButton,
  SocialButton,
  SocialContainer,
  Title,
};
