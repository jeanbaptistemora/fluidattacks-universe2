import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const BlogMainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    roboto
    flex-ns
    flex-wrap-ns
    justify-around
    mw-1366
    ph-body
    pv4-l
    pv3
    bg-graylight
    center
  `,
})``;

const MainBlogCard: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    bs-btm-h-10
    hv-card
    mb5
    relative
    dt-ns
    mt0-ns
    ma-auto
    bg-white
    w-resources-card
  `,
})``;

const CardInnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h30-em
    ph4
  `,
})``;

const CardTitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    c-fluid-bk
    mb0
    tc
    hv-fluid-rd
    lh-solid
  `,
})``;

const CardSubTitle: StyledComponent<
  "h4",
  Record<string, unknown>
> = styled.h4.attrs({
  className: `
    c-fluid-bk
    mb0
    tc
  `,
})``;

const PostInfo: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tl
    pl2
  `,
})``;

const CardText: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw4
    f-1125
    mv0
  `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    f5
    pl2
    mt0
    pt1
    mt2
    mb0
    overflow-hidden
  `,
})``;

const CardButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    absolute
    bottom-2
    right-0
    left-0
    tc
  `,
})``;

const CardButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    hv-bd-fluid-red
    pointer
    white
    pv2
    ph4
    roboto
    fw7
    f5
    dib
    bt-trans
    br2
    bc-fluid-red
    ba
  `,
})``;

const LoadMoreButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    hv-fluid-rd
    hv-card
    t-all-3-eio
    w-100
    roboto
    pv2
    tc
    outline-transparent
    bn
    pointer
  `,
})``;

export {
  BlogMainDiv,
  MainBlogCard,
  CardInnerDiv,
  CardTitle,
  PostInfo,
  CardText,
  CardDescription,
  CardButtonContainer,
  CardButton,
  CardSubTitle,
  LoadMoreButton,
};
