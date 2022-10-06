/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import { Tab } from "./Tab";

const Tabs = styled.ul.attrs({
  className: "comp-tabs list ma0 pa0",
})`
  display: inline-flex;

  > a:first-child,
  > *:first-child a {
    border-radius: 4px 0 0 4px;
  }

  > a:last-child,
  > *:last-child a {
    border-radius: 0 4px 4px 0;
  }

  > a:not(:first-child),
  > *:not(:first-child) a {
    border-left-style: none;
  }
`;

export { Tab, Tabs };
