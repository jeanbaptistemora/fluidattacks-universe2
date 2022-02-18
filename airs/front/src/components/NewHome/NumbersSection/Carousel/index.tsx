import React from "react";

import { NumberCard } from "../NumberCard";
import {
  CarrouselCardsContainer,
  ProgressContainer,
} from "../styledComponents";
import type { INumberCard } from "../types";

interface IProps {
  data: INumberCard;
  progressValue: number;
}

const Carousel: React.FC<IProps> = ({
  data,
  progressValue,
}: IProps): JSX.Element => {
  return (
    <CarrouselCardsContainer>
      <NumberCard
        hasTitle={data.hasTitle}
        image={data.image}
        isGray={data.isGray}
        text={data.text}
        title={data.title}
        typeIcon={data.typeIcon}
      />
      <ProgressContainer>
        <progress max={"5"} value={`${progressValue}`} />
      </ProgressContainer>
    </CarrouselCardsContainer>
  );
};

export { Carousel };
