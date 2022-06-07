import React from "react";

import { ClientCard } from "./ClientCard";
import {
  CardsContainer,
  Container,
  MainTextContainer,
} from "./styledComponents";

import { translate } from "../../../utils/translations/translate";
import { Paragraph, Title } from "../../Texts";

const CardsSection: React.FC = (): JSX.Element => {
  const data = [
    {
      client: translate.t("plansPage.clientsSection.client1.client"),
      description: translate.t("plansPage.clientsSection.client1.description"),
      person: translate.t("plansPage.clientsSection.client1.person"),
    },
    {
      client: translate.t("plansPage.clientsSection.client2.client"),
      description: translate.t("plansPage.clientsSection.client2.description"),
      person: translate.t("plansPage.clientsSection.client2.person"),
    },
    {
      client: translate.t("plansPage.clientsSection.client3.client"),
      description: translate.t("plansPage.clientsSection.client3.description"),
      person: translate.t("plansPage.clientsSection.client3.person"),
    },
  ];

  return (
    <Container>
      <MainTextContainer>
        <Title fColor={"#2e2e38"} fSize={"36"}>
          {translate.t("plansPage.clientsSection.title")}
        </Title>
        <Paragraph fColor={"#5c5c70"} fSize={"24"} marginTop={"2"}>
          {translate.t("plansPage.clientsSection.subtitle")}
        </Paragraph>
      </MainTextContainer>
      <CardsContainer>
        {data.map((card): JSX.Element => {
          return (
            <ClientCard
              client={card.client}
              description={card.description}
              key={card.client}
              person={card.person}
            />
          );
        })}
      </CardsContainer>
    </Container>
  );
};

export { CardsSection };
