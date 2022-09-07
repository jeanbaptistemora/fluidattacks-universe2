/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const CardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    mh2
    mb3
    dt-ns
    mt0-ns
    ma-auto
    hv-card
    relative
    bg-white
    all-card
    bs-btm-h-10
  `,
})`
  max-width: 500px;

  @media screen and (min-width: 1200px) {
    width: 30%;
  }
`;

const WebinarLanguage: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    f7
    c-black-gray
    bg-gray-233
    br4
    pv2
    ph3
    ma0
    fw7
  `,
})``;

const CardTextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ph4
    mh1
  `,
})``;

const CardTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    c-fluid-bk
    mb0
    f3-l
    f3-m
    f4
    b
    lh-solid
    mt2
    roboto
    h-resources-card
  `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    fw3
    f5
    mt1
    h-resources-card
  `,
})``;

const ButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv4
    tc
  `,
})``;

const TextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    w-100
    center
    ph0-ns
    ph3
  `,
})``;

const LittleRegularRedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv3
    ph4
    fw7
    f5
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
    roboto
    mb4
  `,
})``;

const MainCardContainer = styled.div.attrs({
  className: `
    tc
    pv5
    ph4
    mt3
    center
  `,
})`
  background-color: #f4f4f6;
  max-width: 880px;
`;

const ResourcesContainer = styled.div.attrs({
  className: `
    ph-body
  `,
})``;

const FilterButton = styled.button.attrs({
  className: `
    f5
    mh2
    ph3
    pv2
    mv2
    roboto
    pointer
    b--transparent
  `,
})<{ isSelected: boolean }>`
  color: ${({ isSelected }): string => (isSelected ? "#f4f4f6" : "#2e2e38")};
  background-color: ${({ isSelected }): string =>
    isSelected ? "#2e2e38" : "#f4f4f6"};
  border-radius: 2rem;

  :hover {
    background-color: ${({ isSelected }): string =>
      isSelected ? "#2e2e38" : "#b0b0bf"};
  }
`;

const MenuList = styled.div.attrs({
  className: `
      mt3
      flex
      flex-wrap
      justify-center
    `,
})``;

const CardsContainer = styled.div.attrs({
  className: `
    roboto
    flex-ns
    flex-wrap-ns
    justify-around
    mw-1366
    ph-body
    pv4-l
    pv3
    bg-graylight
    center
    `,
})``;

export {
  ButtonContainer,
  CardContainer,
  CardDescription,
  CardsContainer,
  CardTextContainer,
  CardTitle,
  FilterButton,
  LittleRegularRedButton,
  MainCardContainer,
  MenuList,
  ResourcesContainer,
  TextContainer,
  WebinarLanguage,
};
