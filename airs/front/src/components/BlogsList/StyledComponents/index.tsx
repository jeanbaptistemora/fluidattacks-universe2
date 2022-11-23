import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const BlogMainDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    poppins
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
    mb3
    relative
    dt-ns
    mt0-ns
    ma-auto
    bg-white
    w-blog-card
  `,
})``;

const CardInnerDiv: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-blog-card
    ph4
  `,
})``;

const CardTitle: StyledComponent<"p", Record<string, unknown>> = styled.p.attrs(
  {
    className: `
    c-fluid-bk
    mb0
    f3-l
    f3-m
    f4
    b
    hv-fluid-rd
    lh-solid
    mt2
  `,
  }
)`
  min-height: 48px;
`;

const CardSubTitle: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    mb0
    f4
    normal
    mt1
    min-h-60
  `,
})``;

const CardDate: StyledComponent<
  "h5",
  Record<string, unknown>
> = styled.h5.attrs({
  className: `
    c-black-gray
    mb0
  `,
})``;

const PostInfo: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tl
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
    c-gray-120
    f5
    mt0
    pt1
    mt2
    mb0
    overflow-hidden
  `,
})`
  min-height: 100px;
`;

const CardButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv4
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
    poppins
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
    poppins
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
  CardDate,
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
