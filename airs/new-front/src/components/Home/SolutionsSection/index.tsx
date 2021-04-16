/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import { faAngleLeft, faAngleRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "gatsby";
import React, { useEffect, useState } from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import solution1 from "../../../../static/images/solutions/img01.png";
import solution2 from "../../../../static/images/solutions/img02.png";
import solution3 from "../../../../static/images/solutions/img03.png";
import solution4 from "../../../../static/images/solutions/img04.png";
import solution5 from "../../../../static/images/solutions/img05.png";
import solution6 from "../../../../static/images/solutions/img06.png";
import solution7 from "../../../../static/images/solutions/img07.png";
import solution8 from "../../../../static/images/solutions/img08.png";
import { FontAwesomeContainerSmall } from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-700
    mw-1366
    ph-body
    center
    mb1-l
    mb6
  `,
})``;

const InnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex-l
  `,
})``;

const QuarterWidthContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-25-l
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
    fw4
    f5
    ma0
    wm-tb-rl
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-transparent
    bn
    pa3
    dib
    pointer
    outline-transparent
  `,
})``;

const SlideShow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-50-l
    slide-show
    overflow-hidden-l
    overflow-x-auto
    t-all-3-eio
    scroll-smooth
    nowrap
  `,
})``;

const SolutionCard: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-400
    w-300
    mh4
    dib
  `,
})``;

const CardParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    fw4
    f3
    roboto
    mv2
  `,
})``;

const ContinuousContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tl
  `,
})``;

const ContinuousPhrase: StyledComponent<
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

const SolutionsSection: React.FC = (): JSX.Element => {
  const [scroll, setScroll] = useState(0);

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < 364 ? 0 : scroll - 364);
  };

  const scrollRight: () => void = (): void => {
    setScroll(scroll > 2082 ? 2447 : scroll + 364);
  };

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < 2447) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
  };

  useEffect((): void => {
    const slideShow: HTMLElement = document.getElementById(
      "slideShow"
    ) as HTMLElement;
    changeScroll(slideShow);
  });

  return (
    <Container>
      <InnerContainer>
        <QuarterWidthContainer className={"mb4"}>
          <TitleVertical>{"SOLUTIONS"}</TitleVertical>
        </QuarterWidthContainer>
        <QuarterWidthContainer className={"db-l dn tr"}>
          <ArrowButton onClick={scrollLeft}>
            <FontAwesomeContainerSmall>
              <FontAwesomeIcon
                className={"f3 c-black-gray"}
                icon={faAngleLeft}
              />
            </FontAwesomeContainerSmall>
          </ArrowButton>
          <ArrowButton onClick={scrollRight}>
            <FontAwesomeContainerSmall>
              <FontAwesomeIcon
                className={"f3 c-black-gray"}
                icon={faAngleRight}
              />
            </FontAwesomeContainerSmall>
          </ArrowButton>
        </QuarterWidthContainer>
        <SlideShow id={"slideShow"}>
          <Link to={"/solutions/devsecops/"}>
            <SolutionCard>
              <img alt={"DevSecOps"} src={solution1} />
              <CardParagraph>{"DevSecOps"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/security-testing/"}>
            <SolutionCard>
              <img alt={"Security Testing"} src={solution2} />
              <CardParagraph>{"Security Testing"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/penetration-testing/"}>
            <SolutionCard>
              <img alt={"Penetration Testing"} src={solution3} />
              <CardParagraph>{"Penetration Testing"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/ethical-hacking/"}>
            <SolutionCard>
              <img alt={"Ethical Hacking"} src={solution4} />
              <CardParagraph>{"Ethical Hacking"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/red-teaming/"}>
            <SolutionCard>
              <img alt={"Red Teaming"} src={solution5} />
              <CardParagraph>{"Red Teaming"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/attack-simulation/"}>
            <SolutionCard>
              <img alt={"Attack Simulation"} src={solution6} />
              <CardParagraph>{"Attack Simulation"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/secure-code-review/"}>
            <SolutionCard>
              <img alt={"Secure Code Review"} src={solution7} />
              <CardParagraph>{"Secure Code Review"}</CardParagraph>
            </SolutionCard>
          </Link>
          <Link to={"/solutions/vulnerability-management/"}>
            <SolutionCard>
              <img alt={"Vulnerability Management"} src={solution8} />
              <CardParagraph>{"Vulnerability Management"}</CardParagraph>
            </SolutionCard>
          </Link>
        </SlideShow>
      </InnerContainer>
      <ContinuousContainer>
        <ContinuousPhrase className={"c-fluid-bk"}>
          {translate.t("continuousHacking.titleHome")}
        </ContinuousPhrase>
        <ContinuousPhrase className={"c-fluid-gray"}>
          {translate.t("continuousHacking.phraseHome")}
        </ContinuousPhrase>
      </ContinuousContainer>
    </Container>
  );
};

export { SolutionsSection };
