import React from "react";

import { NumberCard } from "../NumberCard";
import { CardsContainer, ProgressContainer } from "../styledComponents";
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
    <CardsContainer>
      <NumberCard
        hasTitle={data.hasTitle}
        image={data.image}
        isGray={data.isGray}
        text={data.text}
        title={data.title}
        typeIcon={data.typeIcon}
      />
      <ProgressContainer>
        <progress max={"100"} value={`${progressValue}`} />
      </ProgressContainer>
    </CardsContainer>
  );
};

export { Carousel };
