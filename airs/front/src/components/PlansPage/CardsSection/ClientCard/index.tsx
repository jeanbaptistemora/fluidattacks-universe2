/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import React from "react";

import { Paragraph, Title } from "../../../Texts";
import { CardContainer, CardDescription } from "../styledComponents";
import type { IClientCard } from "../types";

const ClientCard: React.FC<IClientCard> = ({
  client,
  description,
  person,
}: IClientCard): JSX.Element => {
  return (
    <CardContainer>
      <CardDescription>
        <Paragraph fColor={"#5c5c70"} fSize={"20"}>
          {description}
        </Paragraph>
      </CardDescription>
      <Title fColor={"#5c5c70"} fSize={"24"} marginBottom={"1"} marginTop={"2"}>
        {person}
      </Title>
      <Title fColor={"#ff3435"} fSize={"24"}>
        {client}
      </Title>
    </CardContainer>
  );
};

export { ClientCard };
