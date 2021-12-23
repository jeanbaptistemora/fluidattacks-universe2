import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const InformativeBannerContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    cssmenu
    lh-solid
    h-navbar
    cover
    w-100
    top-0
    z-max
    t-all-linear-3
    bg-fluid-black
  `,
})``;

const BannerItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    mr3
    pr2
    pv4-l
    pv3
  `,
})``;

const BannerButton: StyledComponent<
  "button",
  Record<string, unknown>
> = styled.button.attrs({
  className: `
    outline-transparent
    bg-button-red
    hv-bg-fluid-rd
    pointer
    white
    pv2
    ph3
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

const BannerTitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    white
    fw7
    neue
    lh-solid
    ma0
  `,
})``;

const BannerSubtitle: StyledComponent<
  "h2",
  Record<string, unknown>
> = styled.h2.attrs({
  className: `
    white
    fw1
    neue
    lh-solid
    ma0
  `,
})``;

export {
  BannerButton,
  BannerItem,
  BannerSubtitle,
  BannerTitle,
  InformativeBannerContainer,
};
