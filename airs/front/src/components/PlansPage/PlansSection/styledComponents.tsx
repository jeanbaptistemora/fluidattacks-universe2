/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    center
    flex
    ph-body
  `,
})`
  background-color: #2e2e38;
`;

const PlansContainer = styled.div.attrs({
  className: `
    mv5
    tc
    center
    w-100
  `,
})`
  max-width: 1500px;

  @media (max-width: 960px) {
    max-width: 800px;
  }
`;

const CardsContainer = styled.div.attrs({
  className: `
    flex
    mt5
    justify-center
  `,
})`
  flex-wrap: nowrap;

  @media (max-width: 960px) {
    flex-wrap: wrap;
  }
`;

export { CardsContainer, Container, PlansContainer };
