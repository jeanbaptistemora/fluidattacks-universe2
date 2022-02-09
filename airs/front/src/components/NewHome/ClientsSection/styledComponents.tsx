import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const Container: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    h-500
    bg-darker-blue
    center
    flex
    flex-wrap
    items-center
  `,
})``;

const ClientsContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    mw-1920
    relative
    center
    overflow-hidden
    home-clients-container
  `,
})``;

const TitleContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    tc
    mt4
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
    home-slide-track
    flex
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

export {
  ArrowButton,
  ArrowContainer,
  ClientsContainer,
  Container,
  SlideShow,
  TitleContainer,
};
