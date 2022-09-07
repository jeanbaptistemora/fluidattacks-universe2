/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const Dot = styled.span.attrs({ className: "dib v-top" })`
  margin-left: 3px;
  margin-right: 3px;
  border-radius: 50%;
  height: 6px;
  width: 6px;
  background-color: #bf0b1a;
`;

export { Dot };
