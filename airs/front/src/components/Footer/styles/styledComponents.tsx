import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const FooterMenuContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pb4
    w-100
    tc
    nowrap
    flex-ns
    justify-center
    justify-around-xl
  `,
})``;

const LinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pt4-l
    b
    v-top
    tl
    mh2
    lh-2
  `,
})``;

const FluidLogoContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    fl-xl
    ml-15
    text-center
  `,
})``;
const Container: StyledComponent<
  "footer",
  Record<string, unknown>
> = styled.footer.attrs({
  className: `
    bg-black-18
  `,
})``;

const MainFooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    bg-black-18
    mw-1366
    ph-body
    center
    df-l
    flex-wrap
    pb5-l
    pb5-m
    pb4
    pt4-ns
    pt2
    bw2
    bc-darker-blue
  `,
})``;

export {
  Container,
  FluidLogoContainer,
  FooterMenuContainer,
  LinksContainer,
  MainFooterContainer,
};
