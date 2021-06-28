import type { StyledComponent } from "styled-components";
import styled from "styled-components";

const SubmenuListItem: StyledComponent<
  "li",
  Record<string, unknown>
> = styled.li.attrs({
  className: `
    dib
    ph2
  `,
})``;

const ContentContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    mw-1366
    ph-body
    center
    roboto
  `,
})``;

const CenteredContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    w-100
    pv4
  `,
})``;

const OneShotBlackParagraph: StyledComponent<
  "p",
  Record<string, unknown>
> = styled.p.attrs({
  className: `
    c-fluid-bk
    fw7
    f2
    tc
  `,
})``;

export {
  CenteredContainer,
  ContentContainer,
  OneShotBlackParagraph,
  SubmenuListItem,
};
