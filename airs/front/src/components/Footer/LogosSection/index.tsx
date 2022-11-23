/* eslint import/no-namespace:0 */
/* eslint react/forbid-component-props: 0 */
import React from "react";

import { FullWidthContainer } from "../../../styles/styledComponents";
import { CloudImage } from "../../CloudImage";
import { FluidLogoContainer } from "../styles/styledComponents";

const LogosSection: React.FC = (): JSX.Element => (
  <FullWidthContainer className={"pt4"}>
    <FluidLogoContainer>
      <CloudImage
        alt={"Fluid Attacks logo footer"}
        src={"logo-fluid-dark-2022"}
      />
    </FluidLogoContainer>
  </FullWidthContainer>
);

export { LogosSection };
