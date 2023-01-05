/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React, { useCallback, useEffect, useState } from "react";
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

import { Title } from "../../Texts";

const SolutionsSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      description: t("solutions.homeCards.devSecOps.paragraph"),
      image: "devsecops-card",
      title: t("solutions.homeCards.devSecOps.title"),
      urlCard: "/solutions/devsecops/",
    },
    {
      description: t("solutions.homeCards.secureCode.paragraph"),
      image: "secure-code-card",
      title: t("solutions.homeCards.secureCode.title"),
      urlCard: "/solutions/secure-code-review/",
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
      description: t("solutions.homeCards.securityTesting.paragraph"),
      image: "security-testing-card",
      title: t("solutions.homeCards.securityTesting.title"),
      urlCard: "/solutions/security-testing/",
    },
    {
      description: t("solutions.homeCards.penetrationTesting.paragraph"),
      image: "penetration-testing-card",
      title: t("solutions.homeCards.penetrationTesting.title"),
      urlCard: "/solutions/penetration-testing/",
    },
    {
      description: t("solutions.homeCards.ethicalHacking.paragraph"),
      image: "ethical-hacking-card",
      title: t("solutions.homeCards.ethicalHacking.title"),
      urlCard: "/solutions/ethical-hacking/",
    },
    {
      description: t("solutions.homeCards.vulnerabilityManagement.paragraph"),
      image: "vulnerability-management-card",
      title: t("solutions.homeCards.vulnerabilityManagement.title"),
      urlCard: "/solutions/vulnerability-management/",
    },
  ];

  const cardWidth = 382;
  const maxScroll = cardWidth * data.length;
  const [currentWidth, setCurrentWidth] = useState(0);
  const [scroll, setScroll] = useState(0);

  const scrollLeft: () => void = useCallback((): void => {
    setScroll(scroll < cardWidth ? 0 : scroll - cardWidth);
  }, [scroll]);

  const scrollRight: () => void = useCallback((): void => {
    setScroll(
      scroll > currentWidth - cardWidth ? currentWidth : scroll + cardWidth
    );
  }, [scroll, currentWidth]);

  const changeScroll: (element: HTMLElement) => void = (
    element: HTMLElement
  ): void => {
    if (element.scrollLeft > 0 || element.scrollLeft < currentWidth) {
      element.scrollLeft = scroll;
    } else {
      element.scrollLeft += 0;
    }
    setCurrentWidth(maxScroll - element.offsetWidth);
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
        <Title fColor={"#fff"} fSize={"48"}>
          {t("solutions.homeCards.title")}
        </Title>
      </TitleContainer>
      <CardsContainer>
        <ArrowContainer>
          <ArrowButton limit={scroll === 0} onClick={scrollLeft}>
            <IconContainerSmall>
              <IoIosArrowBack className={"f3 white"} />
            </IconContainerSmall>
          </ArrowButton>
          <ArrowButton limit={scroll === currentWidth} onClick={scrollRight}>
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

export { SolutionsSection };
