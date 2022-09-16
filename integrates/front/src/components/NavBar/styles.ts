/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */
import styled from "styled-components";

const NavBox = styled.nav.attrs({
  className: "Nav",
})`
  align-items: center;
  background-color: #2e2e38;
  border: 1px solid #49495a;
  color: #e9e9ed;
  display: flex;
  justify-content: space-between;
  padding: 4px 20px;
`;

const NavHeader = styled.div``;

const NavMenu = styled.div``;

export { NavBox, NavHeader, NavMenu };
