/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { FullWidthContainer } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";

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
      <CloudImage
        alt={"Fluid Attacks logo footer"}
        src={"logo-fluid-attacks-dark"}
      />
    </FluidLogoContainer>
  </FullWidthContainer>
);

export { LogosSection };
