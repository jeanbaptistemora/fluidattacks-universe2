/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const CardContainer = styled.div.attrs({
  className: `
    mh3
    mb4
    pv4
    ph4
    tc
    br4
    w-100
    center
  `,
})<{ isMachine: boolean }>`
  max-width: 550px;
  margin-top: ${({ isMachine }): string => (isMachine ? "0" : "47px")};
  background-color: ${({ isMachine }): string =>
    isMachine ? "#ffffff" : "#f4f4f6"};
  border-top-left-radius: ${({ isMachine }): string =>
    isMachine ? "unset !important" : "1rem"};
  border-top-right-radius: ${({ isMachine }): string =>
    isMachine ? "unset !important" : "1rem"};
  box-shadow: 0px 0px 6px 3px rgba(0, 0, 0, 0.06);
`;

const CardTitleContainer = styled.div.attrs({
  className: `
    mb3
    tl
  `,
})``;

const CardItemsContainer = styled.div.attrs({
  className: `
    center
    tl
  `,
})``;

const CardItem = styled.div.attrs({
  className: `
    f5
    flex
    pb3
    mb3
    c-black-gray
    roboto
    ma0
    tl
  `,
})``;

const MachineHead = styled.div.attrs({
  className: `
    white
    f4
    dib
    roboto
    w-100
    mh3
    center
  `,
})`
  max-width: 550px;
  padding: 10px 16px;
  background-color: #b0b0bf;
  border-top-left-radius: 1rem;
  border-top-right-radius: 1rem;
`;

export {
  CardContainer,
  CardItem,
  CardItemsContainer,
  CardTitleContainer,
  MachineHead,
};
