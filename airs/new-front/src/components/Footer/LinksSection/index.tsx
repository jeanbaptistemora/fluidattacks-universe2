import React from "react";
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
    flex
    justify-around
  `,
})``;

const LinksContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
    pt4-l
    b
    dib-xl
    display-none
    v-top
    tl
    mh2
  `,
})``;

const LinksSection: React.FC = (): JSX.Element => (
  <FooterMenuContainer>
    <LinksContainer />
  </FooterMenuContainer>
);

export { LinksSection };
