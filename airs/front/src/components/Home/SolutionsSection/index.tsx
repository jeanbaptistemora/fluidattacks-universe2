/* eslint import/no-unresolved:0 */
/* eslint @typescript-eslint/no-magic-numbers:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint import/no-namespace:0 */
/* eslint react/jsx-no-bind:0 */
import { Link } from "gatsby";
import React, { useEffect, useState } from "react";
import ScrollAnimation from "react-animate-on-scroll";
import { FaAngleLeft, FaAngleRight } from "react-icons/fa";

import {
  ArrowButton,
  CardChild,
  CardParagraph,
  CardParent,
  CardsGrid,
  ChildParagraph,
  Container,
  ContinuousContainer,
  ContinuousPhrase,
  InnerContainer,
  SectionTitle,
  SlideShow,
  SolutionCard,
  TitleVertical,
} from "./styledComponents";

import { FontAwesomeContainerSmall } from "../../../styles/styledComponents";
import { translate } from "../../../utils/translations/translate";
import { CloudImage } from "../../CloudImage";

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
                <FaAngleLeft className={"f3 c-black-gray"} />
              </FontAwesomeContainerSmall>
            </ArrowButton>
            <SlideShow id={"slideShow"} style={{ maxWidth: "272px" }}>
              <Link to={"/solutions/devsecops/"}>
                <SolutionCard>
                  <CloudImage alt={"DevSecOps"} src={"devsecops-thumbnail"} />
                  <CardParagraph>{"DevSecOps"}</CardParagraph>
                </SolutionCard>
              </Link>
              <Link to={"/solutions/security-testing/"}>
                <SolutionCard>
                  <CloudImage
                    alt={"Security Testing"}
                    src={"security-testing-thumbnail"}
                  />
                  <CardParagraph>{"Security Testing"}</CardParagraph>
                </SolutionCard>
              </Link>
              <Link to={"/solutions/penetration-testing/"}>
                <SolutionCard>
                  <CloudImage
                    alt={"Penetration Testing"}
                    src={"penetration-testing-thumbnail"}
                  />
                  <CardParagraph>{"Penetration Testing"}</CardParagraph>
                </SolutionCard>
              </Link>
              <Link to={"/solutions/ethical-hacking/"}>
                <SolutionCard>
                  <CloudImage
                    alt={"Ethical Hacking"}
                    src={"ethical-hacking-thumbnail"}
                  />
                  <CardParagraph>{"Ethical Hacking"}</CardParagraph>
                </SolutionCard>
              </Link>
              <Link to={"/solutions/red-teaming/"}>
                <SolutionCard>
                  <CloudImage
                    alt={"Red Teaming"}
                    src={"red-teaming-thumbnail"}
                  />
                  <CardParagraph>{"Red Teaming"}</CardParagraph>
                </SolutionCard>
              </Link>
              <Link to={"/solutions/attack-simulation/"}>
                <SolutionCard>
                  <CloudImage
                    alt={"Attack Simulation"}
                    src={"attack-simulation-thumbnail"}
                  />
                  <CardParagraph>{"Attack Simulation"}</CardParagraph>
                </SolutionCard>
              </Link>
            </SlideShow>
            <ArrowButton onClick={scrollRight}>
              <FontAwesomeContainerSmall>
                <FaAngleRight className={"f3 c-black-gray"} />
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
