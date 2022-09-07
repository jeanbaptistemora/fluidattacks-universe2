/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

import { Indicator } from "./Indicator";

const Indicators = styled.div.attrs({
  className: "flex justify-center pa4",
})`
  background-color: #f4f4f6;
  > div:not(:first-child) {
    border-left: 1px solid #b0b0bf;
    border-radius: 4px;
  }
`;

export { Indicator, Indicators };
