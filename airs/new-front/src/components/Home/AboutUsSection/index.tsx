import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import { translate } from "../../../utils/translations/translate";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-600
    ph-body
    mw-1366
    center
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
  mv5-l
  mv3
  `,
})``;

const PhraseContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
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
    mb7-l
  `,
})`
  writing-mode: tb-rl;
`;

const SectionDefinition: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    roboto
    c-black-gray
    f5
    mt5-l
  `,
})``;

const AboutUsSection: React.FC = (): JSX.Element => (
  <Container>
    <SectionTitleContainer>
      <TitleVertical>{"ABOUT US"}</TitleVertical>
      <SectionDefinition>{translate.t("aboutUs.homePhrase")}</SectionDefinition>
    </SectionTitleContainer>
    <PhraseContainer />
  </Container>
);

export { AboutUsSection };
