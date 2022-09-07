/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const NavbarContainer = styled.nav.attrs({
  className: "flex flex-wrap",
})`
  background-color: #f4f4f6;
  border: 1px solid #d2d2da;
  border-radius: 4px;
  margin: 4px 0;
  padding: 8px 12px;
`;

const NavbarHeader = styled.div.attrs({
  className: "flex flex-auto items-center",
})``;

const NavbarMenu = styled.ul.attrs({
  className: "f4 flex items-center list ma0 ph0",
})`
  & li {
    position: relative;
  }
`;

export { NavbarContainer, NavbarHeader, NavbarMenu };
