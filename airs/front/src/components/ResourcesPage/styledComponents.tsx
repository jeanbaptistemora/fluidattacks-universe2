import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const CardContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fadein
    br3
    bs-btm-h-10
    hv-card
    mb5
    relative
    dt-ns
    mt0-ns
    center
    bg-white
    w-resources-card
    h-resources-card
    all-card
  `,
})``;

const WebinarImageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br3
    br--top
  `,
})``;

const WebinarLanguage: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    f7
    white
    bg-moon-gray
    br3
    pv2
    ph3
    ma0
    fw7
  `,
})``;

const CardTextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ph2
    mh1
  `,
})``;

const CardTitle: StyledComponent<
  "h1",
  Record<string, unknown>
> = styled.h1.attrs({
  className: `
    c-fluid-bk
    mb0
    f3
    fw8
    tc
    lh2
    pb3
    h-resources-card-title
  `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw3
    f5
    mv0
    h-resources-card-description
  `,
})``;

const ButtonContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pv4
    tc
  `,
})``;

const CardInnerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ba1
    mb3
    relative
    dt-ns
    mt0-ns
    pr3-ns
    pl3-ns
    pt3
    ma-auto
    pt3
    ml-auto
    mr-auto
  `,
})``;

const CardInnerTitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    f3
    lh-solid
    c-fluid-bk
    roboto
  `,
})``;

const CardInnerDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    fw3
    f4
    c-fluid-bk
    roboto
  `,
})``;

const ImageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    w-50-l
    mb5
    ml-auto
    mr-auto
  `,
})``;

const TextContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tl-l
    tc
    w-50-l
    mw6
    ml-auto
    mr-auto
    pt3-l
    ph0-ns
    ph3
  `,
})``;

export {
  ButtonContainer,
  CardContainer,
  CardDescription,
  CardInnerContainer,
  CardInnerDescription,
  CardInnerTitle,
  CardTextContainer,
  CardTitle,
  ImageContainer,
  TextContainer,
  WebinarImageContainer,
  WebinarLanguage,
};
