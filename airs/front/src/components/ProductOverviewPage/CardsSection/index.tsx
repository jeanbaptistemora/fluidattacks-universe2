import React from "react";

import { ProductCard } from "./ProductCard";
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
      image: "card-1",
      text: translate.t("productOverview.cardsSection.card1Description"),
      title: translate.t("productOverview.cardsSection.card1Title"),
    },
    {
      image: "card-2",
      text: translate.t("productOverview.cardsSection.card2Description"),
      title: translate.t("productOverview.cardsSection.card2Title"),
    },
    {
      image: "card-3",
      text: translate.t("productOverview.cardsSection.card3Description"),
      title: translate.t("productOverview.cardsSection.card3Title"),
    },
  ];

  return (
    <Container>
      <MainTextContainer>
        <Title fColor={"#2e2e38"} fSize={"36"}>
          {translate.t("productOverview.cardsSection.title")}
        </Title>
        <Paragraph fColor={"#5c5c70"} fSize={"24"} marginTop={"2"}>
          {translate.t("productOverview.cardsSection.paragraph")}
        </Paragraph>
      </MainTextContainer>
      <CardsContainer>
        {data.map((card): JSX.Element => {
          return (
            <ProductCard
              image={card.image}
              key={`card-${card.text}`}
              text={card.text}
              title={card.title}
            />
          );
        })}
      </CardsContainer>
    </Container>
  );
};

export { CardsSection };
