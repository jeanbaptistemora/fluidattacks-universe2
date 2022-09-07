/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { NumberCard } from "../NumberCard";
import {
  CarrouselCardsContainer,
  ProgressBar,
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
        <ProgressBar width={`${progressValue}%`} />
      </ProgressContainer>
    </CarrouselCardsContainer>
  );
};

export { Carousel };
