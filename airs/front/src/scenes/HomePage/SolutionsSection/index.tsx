/* eslint react/forbid-component-props: 0 */
/* eslint fp/no-mutation:0 */
/* eslint react/jsx-no-bind:0 */
import React from "react";
import { useTranslation } from "react-i18next";
import { BsArrowRight } from "react-icons/bs";

import {
  CardFooter,
  MainCoverHome,
  SlideShow,
  SolutionsContainer,
} from "./styledComponents";

import { AirsLink } from "../../../components/AirsLink";
import { Button } from "../../../components/Button";
import { Container } from "../../../components/Container";
import { Text, Title } from "../../../components/Typography";

const SolutionsSection: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const data = [
    {
      description: t("solutions.homeCards.devSecOps.paragraph"),
      title: t("solutions.homeCards.devSecOps.title"),
      urlCard: "/solutions/devsecops/",
    },
    {
      description: t("solutions.homeCards.secureCode.paragraph"),
      title: t("solutions.homeCards.secureCode.title"),
      urlCard: "/solutions/secure-code-review/",
    },
    {
      description: t("solutions.homeCards.redTeaming.paragraph"),
      title: t("solutions.homeCards.redTeaming.title"),
      urlCard: "/solutions/red-teaming/",
    },
    {
      description: t("solutions.homeCards.attackSimulation.paragraph"),
      title: t("solutions.homeCards.attackSimulation.title"),
      urlCard: "/solutions/attack-simulation/",
    },
    {
      description: t("solutions.homeCards.securityTesting.paragraph"),
      title: t("solutions.homeCards.securityTesting.title"),
      urlCard: "/solutions/security-testing/",
    },
    {
      description: t("solutions.homeCards.penetrationTesting.paragraph"),
      title: t("solutions.homeCards.penetrationTesting.title"),
      urlCard: "/solutions/penetration-testing/",
    },
    {
      description: t("solutions.homeCards.ethicalHacking.paragraph"),
      title: t("solutions.homeCards.ethicalHacking.title"),
      urlCard: "/solutions/ethical-hacking/",
    },
    {
      description: t("solutions.homeCards.vulnerabilityManagement.paragraph"),
      title: t("solutions.homeCards.vulnerabilityManagement.title"),
      urlCard: "/solutions/vulnerability-management/",
    },
  ];

  return (
    <MainCoverHome>
      <Container>
        <Container
          align={"center"}
          center={true}
          display={"flex"}
          justify={"center"}
          maxWidth={"850px"}
          mb={4}
          minHeight={"360px"}
          wrap={"wrap"}
        >
          <Title
            color={"#ffffff"}
            level={1}
            mb={4}
            mt={5}
            size={"medium"}
            textAlign={"center"}
          >
            {t("home.solutions.title")}
          </Title>
          <Text color={"#b0b0bf"} mb={4} size={"big"} textAlign={"center"}>
            {t("home.solutions.subtitle")}
          </Text>
          <AirsLink href={"/solutions/"}>
            <Button display={"block"} variant={"primary"}>
              <Text color={"inherit"}>{"Learn more"}</Text>
            </Button>
          </AirsLink>
        </Container>
        <SolutionsContainer gradientColor={"#fffff"}>
          <SlideShow>
            {[...Array(2).keys()].map((): JSX.Element[] =>
              data.map(
                (card): JSX.Element => (
                  <Container
                    align={"start"}
                    bgGradient={"#ffffff, #f4f4f6"}
                    borderColor={"#dddde3"}
                    borderHoverColor={"#bf0b1a"}
                    br={2}
                    direction={"column"}
                    display={"flex"}
                    height={"318px"}
                    hoverColor={"#ffe5e7"}
                    key={card.urlCard}
                    ph={3}
                    pv={3}
                    width={"338px"}
                  >
                    <Title color={"#bf0b1a"} level={4} size={"xxs"}>
                      {"SOLUTION"}
                    </Title>
                    <Title
                      color={"#2e2e38"}
                      level={4}
                      mb={3}
                      mt={3}
                      size={"small"}
                    >
                      {card.title}
                    </Title>
                    <Text color={"#535365"} size={"medium"}>
                      {card.description}
                    </Text>
                    <CardFooter>
                      <Container
                        align={"center"}
                        display={"flex"}
                        pb={2}
                        wrap={"wrap"}
                      >
                        <AirsLink
                          decoration={"underline"}
                          hoverColor={"#bf0b1a"}
                          href={card.urlCard}
                        >
                          <Text
                            color={"#2e2e38"}
                            mr={1}
                            size={"small"}
                            weight={"bold"}
                          >
                            {"Read more"}
                          </Text>
                        </AirsLink>
                        <BsArrowRight size={10} />
                      </Container>
                    </CardFooter>
                  </Container>
                )
              )
            )}
          </SlideShow>
        </SolutionsContainer>
      </Container>
    </MainCoverHome>
  );
};

export { SolutionsSection };
