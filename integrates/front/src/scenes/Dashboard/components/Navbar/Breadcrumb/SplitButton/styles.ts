/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import styled from "styled-components";

const SplitButtonContainer = styled.button.attrs({
  className: "bn bg-transparent relative dib pointer pv2",
})`
  color: #2e2e38;
  :hover {
    color: #ff3435;
  }
`;

export { SplitButtonContainer };
