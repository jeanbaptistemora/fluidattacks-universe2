import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const AdvisoriesShadowBoxContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    dib
    f-1125
    lh-copy
    mb4
    mh4
    relative
    bs-btm-h-10
    h-advisories-card
  `,
})``;
const AdvisoriesCardFront: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-white
    br3
    h-100
    pa4
    tl
  `,
})``;
const AdvisoriesCardFrontTitle: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    f6
    shadow-gray
    tracked
    roboto
  `,
})``;
const AdvisoriesCardFrontDesc: StyledComponent<
  "h4",
  Record<string, unknown>
> = styled.h4.attrs({
  className: `
    f3
    mv0
    neue
  `,
})``;
const AdvisoriesCardFrontAuthorContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    items-center
    flex
  `,
})``;
const AdvisoriesCardBack: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    absolute
    advisor-animation
    advisor-transition
    bg-white
    br3
    left-0
    pa4
    tc
    top-0
    h-100
  `,
})``;
const AdvisoriesCardBackList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
    list
    ma0
    pa0
    mb2
    h-advisories-card-back-list
  `,
})``;
const AdvisoriesCardBackItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    dib
    f-1125
    lh-2
    relative
    tl
    w-100
    roboto
  `,
})``;

export {
  AdvisoriesCardBack,
  AdvisoriesCardBackItem,
  AdvisoriesCardBackList,
  AdvisoriesCardFront,
  AdvisoriesCardFrontAuthorContainer,
  AdvisoriesCardFrontDesc,
  AdvisoriesCardFrontTitle,
  AdvisoriesShadowBoxContainer,
};
