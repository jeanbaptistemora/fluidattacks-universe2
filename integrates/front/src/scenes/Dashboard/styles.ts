/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-row h-100",
})`
  background-color: #e9e9ed;
  color: #2e2e38;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
`;

const DashboardContent = styled.div.attrs({
  className: "flex flex-auto flex-column",
})`
  overflow-y: auto;
  padding-bottom: 72px;
  padding-left: 24px;
  padding-right: 24px;

  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-track {
    background: #b0b0bf;
  }
  ::-webkit-scrollbar-thumb {
    background: #65657b;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #535365;
  }
`;

const DashboardHeader = styled.header.attrs({
  className: "top-0 z-5",
})``;

export { DashboardContainer, DashboardContent, DashboardHeader };
