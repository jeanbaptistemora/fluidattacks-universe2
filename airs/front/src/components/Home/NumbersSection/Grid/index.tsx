/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { NumberCard } from "../NumberCard";
import { GridCardsContainer } from "../styledComponents";
import type { INumberCard } from "../types";

interface IProps {
  data: INumberCard[];
}

const Grid: React.FC<IProps> = ({ data }: IProps): JSX.Element => {
  return (
    <GridCardsContainer>
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
    </GridCardsContainer>
  );
};

export { Grid };
