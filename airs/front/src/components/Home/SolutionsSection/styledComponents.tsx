import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-700
    mw-1366
    center
    mb1-l
    mb6
  `,
})``;

const InnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    flex-l
  `,
})``;

const SectionTitle: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-40-l
  `,
})``;

const TitleVertical: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    tl
    rotate-180
    roboto
    c-black-gray
    fw4
    f5
    ma0
    wm-tb-rl
    ph-body
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-transparent
    bn
    dib
    pointer
    outline-transparent
    pv5
  `,
})``;

const CardsGrid: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-50-l
    db-l
    dn
  `,
})``;

const CardParent: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    card-parent
    ma2
    pointer
    fl
    relative
    mb4
  `,
})``;

const CardChild: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-100
    w-100
    card-child
    cover
    bg-center
    t-all-5
    flex
    justify-center
    items-center
  `,
})``;

const SlideShow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    slide-show
    overflow-hidden-l
    overflow-x-auto
    t-all-3-eio
    scroll-smooth
    nowrap
    dn-l
  `,
})``;

const SolutionCard: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-300
    mh4
    dib
  `,
})``;

const CardParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    fw4
    f5
    roboto
    mv2
  `,
})``;

const ChildParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    card-link
    absolute
    white
    roboto
  `,
})``;

const ContinuousContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tl
    ph-body
  `,
})``;

const ContinuousPhrase: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    mv0
    neue
    f3
    tl
    fw7
  `,
})``;

export {
  ArrowButton,
  CardChild,
  CardParagraph,
  CardParent,
  CardsGrid,
  ChildParagraph,
  Container,
  ContinuousContainer,
  ContinuousPhrase,
  InnerContainer,
  SectionTitle,
  SlideShow,
  SolutionCard,
  TitleVertical,
};
