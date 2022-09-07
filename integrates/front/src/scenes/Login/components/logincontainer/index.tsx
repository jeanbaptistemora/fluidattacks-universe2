/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import style from "scenes/Login/components/logincontainer/index.css";

const LoginContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `${style.container} h-100 flex items-center justify-center mv0 center overflow-y-auto-l overflow-y-hidden-m overflow-y-hidden`,
})``;

export { LoginContainer };
