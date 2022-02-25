/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { IoIosArrowBack, IoIosArrowForward } from "react-icons/io";

import { SolutionCard } from "./SolutionCard";
import {
  ArrowButton,
  ArrowContainer,
  CardsContainer,
  Container,
  IconContainerSmall,
  SlideShow,
  TitleContainer,
} from "./styledComponents";

import { WhiteBigParagraph } from "../../../styles/styledComponents";

const SolutionSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      description: t("solutions.homeCards.devSecOps.paragraph"),
      image: "devsecops-card",
      title: t("solutions.homeCards.devSecOps.title"),
      urlCard: "/solutions/devsecops/",
    },
    {
      description: t("solutions.homeCards.ethicalHacking.paragraph"),
      image: "ethical-hacking-card",
      title: t("solutions.homeCards.ethicalHacking.title"),
      urlCard: "/solutions/ethical-hacking/",
    },
    {
      description: t("solutions.homeCards.securityTesting.paragraph"),
      image: "security-testing-card",
      title: t("solutions.homeCards.securityTesting.title"),
      urlCard: "/solutions/security-testing/",
    },
    {
      description: t("solutions.homeCards.redTeaming.paragraph"),
      image: "red-teaming-card",
      title: t("solutions.homeCards.redTeaming.title"),
      urlCard: "/solutions/red-teaming/",
    },
    {
      description: t("solutions.homeCards.attackSimulation.paragraph"),
      image: "attack-simulation-card",
      title: t("solutions.homeCards.attackSimulation.title"),
      urlCard: "/solutions/attack-simulation/",
    },
    {
      description: t("solutions.homeCards.secureCode.paragraph"),
      image: "secure-code-card",
      title: t("solutions.homeCards.secureCode.title"),
      urlCard: "/solutions/secure-code-review/",
    },
    {
      description: t("solutions.homeCards.vulnerabilityManagement.paragraph"),
      image: "vulnerability-management-card",
      title: t("solutions.homeCards.vulnerabilityManagement.title"),
      urlCard: "/solutions/vulnerability-management/",
    },
    {
      description: t("solutions.homeCards.penetrationTesting.paragraph"),
      image: "penetration-testing-card",
      title: t("solutions.homeCards.penetrationTesting.title"),
      urlCard: "/solutions/penetration-testing/",
    },
  ];

  const cardWidth = 382;
  const maxScroll = cardWidth * data.length;
  const [width, setwidth] = useState(0);
  const [scroll, setScroll] = useState(0);

  const scrollLeft: () => void = (): void => {
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  };

  const scrollRight: () => void = (): void => {
    setScroll(scroll > width - cardWidth ? width : scroll + cardWidth);
  };

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < width) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
    setwidth(maxScroll - element.offsetWidth);
  };

  useEffect((): void => {
    const slideShow: HTMLElement = document.getElementById(
      "solutionsSlides"
    ) as HTMLElement;
    changeScroll(slideShow);
  });

  return (
    <Container>
      <TitleContainer>
        <WhiteBigParagraph>{t("solutions.homeCards.title")}</WhiteBigParagraph>
      </TitleContainer>
      <CardsContainer>
        <ArrowContainer>
          <ArrowButton onClick={scrollLeft}>
            <IconContainerSmall>
              <IoIosArrowBack className={"f3 white"} />
            </IconContainerSmall>
          </ArrowButton>
          <ArrowButton onClick={scrollRight}>
            <IconContainerSmall>
              <IoIosArrowForward className={"f3 white"} />
            </IconContainerSmall>
          </ArrowButton>
        </ArrowContainer>
        <SlideShow id={"solutionsSlides"}>
          {data.map((card): JSX.Element => {
            return (
              <SolutionCard
                description={card.description}
                image={card.image}
                key={card.title}
                title={card.title}
                urlCard={card.urlCard}
              />
            );
          })}
        </SlideShow>
      </CardsContainer>
    </Container>
  );
};

export { SolutionSection };
