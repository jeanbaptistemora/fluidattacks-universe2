/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Container = styled.div.attrs({
  className: "flex flex-row h-100",
})`
  background-color: #e9e9ed;
  color: #2e2e38;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
`;

const DashboardContent = styled.div.attrs({
  className: "flex flex-auto flex-column overflow-container",
})`
  padding-left: 24px;
  padding-right: 24px;

  // Hide scrollbar for Chrome, Safari and Opera
  ::-webkit-scrollbar {
    display: none;
  }
  // Hide scrollbar for IE, Edge and Firefox
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

export { Container, DashboardContent };
