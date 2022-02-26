/* eslint react/forbid-component-props: 0 */
import React from "react";

import { InfoSection } from "./InfoSection";
import { LinksSection } from "./LinksSection";
import { LogosSection } from "./LogosSection";
import { Container, MainFooterContainer } from "./styles/styledComponents";

import {
  CenteredMaxWidthContainer,
  MainFooterInfoContainer,
} from "../../styles/styledComponents";

const Footer: React.FC = (): JSX.Element => (
  <Container>
    <MainFooterContainer>
      <LogosSection />
      <LinksSection />
      <MainFooterInfoContainer>
        <CenteredMaxWidthContainer className={"pv3"}>
          <InfoSection />
        </CenteredMaxWidthContainer>
      </MainFooterInfoContainer>
    </MainFooterContainer>
  </Container>
);

export { Footer };
