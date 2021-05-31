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
      pt6-l
      pt5
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
    `,
})``;

const BlogFooterColsHeader: StyledComponent<
  "b",
  Record<string, unknown>
> = styled.b.attrs({
  className: `
    flex
    mv3
    `,
})``;

const RedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    roboto
    w-auto-l
    w-100
    h-100
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv3
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
