/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { InfoSection } from "./InfoSection";
import { LinksSection } from "./LinksSection";
import { LogosSection } from "./LogosSection";

import {
  CenteredMaxWidthContainer,
  MainFooterInfoContainer,
} from "../../styles/styledComponents";

const DarkBlueFooter: StyledComponent<
  "footer",
  Record<string, unknown>
> = styled.footer.attrs({
  className: `
    bg-darker-blue
  `,
})``;

const MainFooterContainer: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs({
  className: `
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
    ba
    bw2
    bc-darker-blue
  `,
})``;

const Footer: React.FC = (): JSX.Element => (
  <DarkBlueFooter>
    <MainFooterContainer>
      <LogosSection />
      <LinksSection />
      <MainFooterInfoContainer>
        <CenteredMaxWidthContainer className={"pv3"}>
          <InfoSection />
        </CenteredMaxWidthContainer>
      </MainFooterInfoContainer>
    </MainFooterContainer>
  </DarkBlueFooter>
);

export { Footer };
