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
import ScrollAnimation from "react-animate-on-scroll";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import solution1 from "../../../../static/images/solutions/img01.png";
import solution2 from "../../../../static/images/solutions/img02.png";
import solution3 from "../../../../static/images/solutions/img03.png";
import solution4 from "../../../../static/images/solutions/img04.png";
import solution5 from "../../../../static/images/solutions/img05.png";
import solution6 from "../../../../static/images/solutions/img06.png";
import { FontAwesomeContainerSmall } from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-700
    mw-1366
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

const SectionTitle: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-40-l
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
    ph-body
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-transparent
    bn
    dib
    pointer
    outline-transparent
    pv5
  `,
})``;

const CardsGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-60-l
    db-l
    dn
  `,
})``;

const CardParent: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    card-parent
    ma2
    pointer
    fl
    relative
    mb4
  `,
})``;

const CardChild: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-100
    card-child
    cover
    bg-center
    t-all-5
    flex
    justify-center
    items-center
  `,
})``;

const SlideShow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    slide-show
    overflow-hidden-l
    overflow-x-auto
    t-all-3-eio
    scroll-smooth
    nowrap
    dn-l
  `,
})``;

const SolutionCard: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
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
    f5
    roboto
    mv2
  `,
})``;

const ChildParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    card-link
    absolute
    white
    roboto
  `,
})``;

const ContinuousContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tl
    ph-body
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
    setScroll(scroll < 272 ? 0 : scroll - 272);
  };

  const scrollRight: () => void = (): void => {
    setScroll(scroll > 1080 ? 1360 : scroll + 272);
  };

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < 1360) {
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
    <ScrollAnimation animateIn={"animate__fadeIn"} animateOnce={true} delay={5}>
      <Container>
        <InnerContainer>
          <SectionTitle className={"mb4"}>
            <TitleVertical>{"SOLUTIONS"}</TitleVertical>
          </SectionTitle>
          <CardsGrid>
            <CardParent>
              <Link to={"/solutions/devsecops/"}>
                <CardChild className={"bg-solution1"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"DevSecOps"}</CardParagraph>
            </CardParent>
            <CardParent>
              <Link to={"/solutions/security-testing/"}>
                <CardChild className={"bg-solution2"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"Security Testing"}</CardParagraph>
            </CardParent>
            <CardParent>
              <Link to={"/solutions/penetration-testing/"}>
                <CardChild className={"bg-solution3"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"Penetration Testing"}</CardParagraph>
            </CardParent>
            <CardParent>
              <Link to={"/solutions/ethical-hacking/"}>
                <CardChild className={"bg-solution4"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"Ethical Hacking"}</CardParagraph>
            </CardParent>
            <CardParent>
              <Link to={"/solutions/red-teaming/"}>
                <CardChild className={"bg-solution5"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"Red Teaming"}</CardParagraph>
            </CardParent>
            <CardParent>
              <Link to={"/solutions/attack-simulation/"}>
                <CardChild className={"bg-solution6"}>
                  <ChildParagraph>{"Go to Solution"}</ChildParagraph>
                </CardChild>
              </Link>
              <CardParagraph>{"Attack Simulation"}</CardParagraph>
            </CardParent>
          </CardsGrid>
          <div className={"flex dn-l justify-center items-center"}>
            <ArrowButton onClick={scrollLeft}>
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon
                  className={"f3 c-black-gray"}
                  icon={faAngleLeft}
                />
              </FontAwesomeContainerSmall>
            </ArrowButton>
            <SlideShow id={"slideShow"} style={{ maxWidth: "272px" }}>
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
            </SlideShow>
            <ArrowButton onClick={scrollRight}>
              <FontAwesomeContainerSmall>
                <FontAwesomeIcon
                  className={"f3 c-black-gray"}
                  icon={faAngleRight}
                />
              </FontAwesomeContainerSmall>
            </ArrowButton>
          </div>
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
    </ScrollAnimation>
  );
};

export { SolutionsSection };
