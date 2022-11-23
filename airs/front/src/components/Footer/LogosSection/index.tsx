/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
        src={"logo-fluid-attacks-dark"}
      />
    </FluidLogoContainer>
  </FullWidthContainer>
);

export { LogosSection };
