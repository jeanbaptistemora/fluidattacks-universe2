import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-500
    mw-1366
    center
    flex-l
    mb1-l
    mb6
  `,
})``;

const ClientsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    br
    b--light-gray
  `,
})``;

const ClientsTitle: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    neue
    f3
    tl
    fw7
    c-fluid-bk
    pv4
    ph-body
  `,
})``;

const ArrowButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    bg-fluid-gray
    bn
    pa3
    dib
    pointer
    outline-transparent
  `,
})``;

const SlideShow: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    slide-show
    overflow-hidden-l
    overflow-x-auto
    t-all-3-eio
    scroll-smooth
    nowrap
    mw-446
    center
  `,
})``;

const ArrowContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bt
    b--light-gray
    tr
  `,
})``;

const DefinitionContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    ph-body
    flex
    justify-center
    items-center
  `,
})``;

const DefinitionParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    roboto
    c-black-gray
    fw4
    f5
    lh-copy
    mv4
    mw7-l
    mw6
  `,
})``;

export {
  ArrowButton,
  ArrowContainer,
  ClientsContainer,
  ClientsTitle,
  Container,
  DefinitionContainer,
  DefinitionParagraph,
  SlideShow,
};
