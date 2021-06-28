import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const LanguagesListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  mw-1366
  ph-body
  center
  pv5
  v-top
  mb5
  roboto
`,
})``;
const ListContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  center
  moon-gray
  mw8
`,
})``;
const ListColumn: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
  list
  roboto
  f3-ns
  f4
  fw7
  dib-l
  ph4
  mv0
  pv0-l
  pv4
  tl
`,
})``;
const SastParagraph: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    center
    roboto
    f3-l
    f4
    lh-2
    pv4
  `,
})``;

export { LanguagesListContainer, ListColumn, ListContainer, SastParagraph };
