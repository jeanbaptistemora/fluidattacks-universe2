import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-600
    ph-body
    mw-1366
    center
    mb1-ns
    mb6
  `,
})``;

const SectionTitleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-34-l
    fl-l
    center
    br-l
    bw2
    b--light-gray
  `,
})``;

const PhraseContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-60-l
    fr-l
    ma0-l
    pa0-l
    center
  `,
})``;

const TitleVertical: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tl
    rotate-180
    roboto
    c-black-gray
    f5
    mh0
    wm-tb-rl
    mb7-l
  `,
})``;

const SectionDefinition: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    roboto
    c-black-gray
    fw4
    f5
    mt5-l
    mr3-l
    lh-copy
  `,
})``;

const PhraseParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    mv0
    neue
    f3
    tl
    fw7
  `,
})``;

export {
  Container,
  PhraseContainer,
  PhraseParagraph,
  SectionDefinition,
  SectionTitleContainer,
  TitleVertical,
};
