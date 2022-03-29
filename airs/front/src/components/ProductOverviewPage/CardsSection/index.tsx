import React from "react";

import { ProductCard } from "./ProductCard";
import { Container } from "./styledComponents";

import { translate } from "../../../utils/translations/translate";

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
    </Container>
  );
};

export { CardsSection };
