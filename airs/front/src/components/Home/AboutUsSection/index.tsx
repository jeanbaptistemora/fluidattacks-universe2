import React from "react";
import ScrollAnimation from "react-animate-on-scroll";

import {
  Container,
  PhraseContainer,
  PhraseParagraph,
  SectionDefinition,
  SectionTitleContainer,
  TitleVertical,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

const AboutUsSection: React.FC = (): JSX.Element => (
  <Container>
    <SectionTitleContainer>
      <TitleVertical>{"ABOUT US"}</TitleVertical>
      <SectionDefinition>
        {translate.t("aboutUs.homeSmallPhrase")}
      </SectionDefinition>
    </SectionTitleContainer>
    <PhraseContainer>
      <ScrollAnimation animateIn={"animate__fadeInUp"} animateOnce={true}>
        <PhraseParagraph>
          <b className={"c-fluid-bk fw7"}>
            {`${translate.t("aboutUs.homeBlackPhrase")} `}
          </b>
          <b className={"c-fluid-gray fw7"}>
            {translate.t("aboutUs.homeGrayPhrase")}
          </b>
        </PhraseParagraph>
      </ScrollAnimation>
    </PhraseContainer>
  </Container>
);

export { AboutUsSection };
