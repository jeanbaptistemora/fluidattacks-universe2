import React from "react";

import { NumberCard } from "../NumberCard";
import { CardsContainer } from "../styledComponents";
import type { INumberCard } from "../types";

interface IProps {
  data: INumberCard;
}

const Carousel: React.FC<IProps> = ({ data }: IProps): JSX.Element => {
  return (
    <CardsContainer>
      <NumberCard
        hasTitle={data.hasTitle}
        image={data.image}
        isGray={data.isGray}
        text={data.text}
        title={data.title}
        typeIcon={data.typeIcon}
      />
    </CardsContainer>
  );
};

export { Carousel };
