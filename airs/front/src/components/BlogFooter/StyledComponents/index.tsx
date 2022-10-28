/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const BlogFooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    flex-wrap
    w-100
    tl
    pt3
    mw6-m
    ml-auto
    mr-auto
    justify-center
  `,
})``;

const BlogFooterCols: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ma2
    blog-footer-col
  `,
})``;

const BlogFooterColsBody: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex
    c-fluid-bk
    fw4
    f-1125
    v-mid
    mr4-l
    pv0-l
    pv3
    mv1
    justify-center
    justify-start-l
  `,
})``;

const BlogFooterColsHeader: StyledComponent<
  "b",
  Record<string, unknown>
> = styled.b.attrs({
  className: `
    flex
    mv3-l
    mv1
    justify-center
    justify-start-l
  `,
})``;

const RedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    poppins
    w-auto-l
    w-100
    h-100
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    ph5
    fw4
    f5
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
  `,
})``;

export {
  BlogFooterCols,
  BlogFooterColsBody,
  BlogFooterColsHeader,
  BlogFooterContainer,
  RedButton,
};
