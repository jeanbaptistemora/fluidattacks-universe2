/* eslint react/forbid-component-props: 0 */
import React from "react";

import { InfoSection } from "./InfoSection";
import { LinksSection } from "./LinksSection";
import { LogosSection } from "./LogosSection";
import { DarkBlueFooter, MainFooterContainer } from "./styles/styledComponents";

import {
  CenteredMaxWidthContainer,
  MainFooterInfoContainer,
} from "../../styles/styledComponents";

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
