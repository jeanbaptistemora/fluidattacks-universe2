/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import fluidAttacksLogo from "../../../../static/images/logo-fluid-attacks-dark.png";
import { FullWidthContainer } from "../../../styles/styledComponents";

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

const LogosSection: React.FC = (): JSX.Element => (
  <FullWidthContainer className={"pt4"}>
    <FluidLogoContainer>
      <img alt={"Fluid Attacks logo footer"} src={fluidAttacksLogo} />
    </FluidLogoContainer>
  </FullWidthContainer>
);

export { LogosSection };
