/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const MainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  vh-100
  thank-you-bg
  items-center
  justify-center
  flex
  bg-center
`,
})``;
const InnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  w-100
  tc
`,
})``;
const TitleDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  poppins
  c-fluid-bk
  f2
  fw7
  tc
  lh-solid
`,
})``;
const ContentMainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  w36-l
  center
`,
})``;
const ContentInnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  poppins
  f4
  c-fluid-bk
  fw3
  tc
`,
})``;
const ButtonDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
  dib
  tc
  w-100-s
  w-100-m
  pv3
`,
})``;

export {
  ButtonDiv,
  ContentInnerDiv,
  ContentMainDiv,
  InnerDiv,
  MainDiv,
  TitleDiv,
};
