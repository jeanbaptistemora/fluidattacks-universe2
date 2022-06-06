import React from "react";

import { PlanCard } from "./PlanCard";
import { CardsContainer, Container, PlansContainer } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { Paragraph, Title } from "../../Texts";

const PlansSection: React.FC = (): JSX.Element => {
  const data = [
    {
      description: translate.t(
        "productOverview.plansSection.plansCards.machineDescription"
      ),
      isMachine: true,
      items: [
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item1"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item2"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item3"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item4"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item5"),
        },
        {
          check: false,
          text: translate.t("productOverview.plansSection.plansCards.item6"),
        },
        {
          check: false,
          text: translate.t("productOverview.plansSection.plansCards.item7"),
        },
        {
          check: false,
          text: translate.t("productOverview.plansSection.plansCards.item8"),
        },
        {
          check: false,
          text: translate.t("productOverview.plansSection.plansCards.item9"),
        },
        {
          check: false,
          text: translate.t("productOverview.plansSection.plansCards.item10"),
        },
      ],
      title: translate.t(
        "productOverview.plansSection.plansCards.machineTitle"
      ),
    },
    {
      description: translate.t(
        "productOverview.plansSection.plansCards.squadDescription"
      ),
      isMachine: false,
      items: [
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item1"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item2"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item3"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item4"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item5"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item6"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item7"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item8"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item9"),
        },
        {
          check: true,
          text: translate.t("productOverview.plansSection.plansCards.item10"),
        },
      ],
      title: translate.t("productOverview.plansSection.plansCards.squadTitle"),
    },
  ];

  return (
    <Container>
      <PlansContainer>
        <Title fColor={"#f4f4f6"} fSize={"48"} marginBottom={"1"}>
          {translate.t("productOverview.plansSection.title")}
        </Title>
        <Paragraph fColor={"#f4f4f6"} fSize={"24"}>
          {translate.t("productOverview.plansSection.description")}
        </Paragraph>
        <CardsContainer>
          {data.map((card): JSX.Element => {
            return (
              <PlanCard
                description={card.description}
                isMachine={card.isMachine}
                items={card.items}
                key={card.title}
                title={card.title}
              />
            );
          })}
        </CardsContainer>
      </PlansContainer>
    </Container>
  );
};

export { PlansSection };
