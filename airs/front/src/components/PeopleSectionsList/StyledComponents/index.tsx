/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const SectionContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      h-section
      flex
      items-center
      justify-center
      flex-wrap
    `,
})``;
const SectionTitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
      c-fluid-bk
      fw7
      f2
      mv0
      tl
      lh-18
    `,
})``;
const SectionDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
      c-fluid-bk
      fw3
      f-solution
      lh-2
      tl
      f3
    `,
})``;
const LeftColumn: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      fl-l
      pr4-l
      w-50-l
    `,
})``;
const RightColumn: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
      fr-l
      pl4-l
      w-50-l
    `,
})``;

export {
  LeftColumn,
  RightColumn,
  SectionContainer,
  SectionDescription,
  SectionTitle,
};
