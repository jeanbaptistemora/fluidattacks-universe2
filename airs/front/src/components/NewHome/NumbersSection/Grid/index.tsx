import React from "react";

import { NumberCard } from "../NumberCard";
import { CardsContainer } from "../styledComponents";
import type { INumberCard } from "../types";

interface IProps {
  data: INumberCard[];
}

const Grid: React.FC<IProps> = ({ data }: IProps): JSX.Element => {
  return (
    <CardsContainer>
      {data.map((card): JSX.Element => {
        return (
          <NumberCard
            hasTitle={card.hasTitle}
            image={card.image}
            isGray={card.isGray}
            key={`card-${card.text}`}
            text={card.text}
            title={card.title}
            typeIcon={card.typeIcon}
          />
        );
      })}
    </CardsContainer>
  );
};

export { Grid };
