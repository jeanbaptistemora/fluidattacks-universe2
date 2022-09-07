/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";
import "./index.css";

const LoginGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "br2 flex justify-center flex-column login-grid pa4",
})`
  background-color: #f4f4f6;
`;

export { LoginGrid };
