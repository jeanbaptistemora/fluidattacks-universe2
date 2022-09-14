/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const SideBarBox = styled.div.attrs({
  className: "SideBar h-100",
})`
  background-color: #2e2e38;
  color: #c7c7d1;
  display: inline-block;
  min-width: 150px;
  padding: 12px 0;

  > div > hr:not(:first-child) {
    display: none;
  }
`;

const SideBarHr = styled.hr`
  border-top: 1px solid #65657b;
  margin: 2px 20px;
`;

export { SideBarBox, SideBarHr };
