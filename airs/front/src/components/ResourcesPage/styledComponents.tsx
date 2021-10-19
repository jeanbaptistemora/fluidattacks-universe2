import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const CardContainer: StyledComponent<
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
    all-card
  `,
})``;

const WebinarLanguage: StyledComponent<
  "span",
  Record<string, unknown>
> = styled.span.attrs({
  className: `
    f7
    c-black-gray
    bg-gray-233
    br4
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
    ph4
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
    f3-l
    f3-m
    f4
    b
    lh-solid
    mt2
    min-h-60
    roboto
  `,
})``;

const CardDescription: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-black-gray
    fw3
    f5
    mt1
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
    pt3
    center
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
    f5
    c-black-gray
    roboto
  `,
})``;

const ImageContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    tc
    w-100
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
    tc
    w-100
    center
    ph0-ns
    ph3
  `,
})``;

const LittleRegularRedButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv3
    ph4
    fw7
    f5
    dib
    t-all-3-eio
    br2
    bc-fluid-red
    ba
    roboto
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
  LittleRegularRedButton,
  TextContainer,
  WebinarLanguage,
};
