/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";

import { CardsSection } from "./CardsSection";
import { Comparative } from "./Comparative";
import { PlansSection } from "./PlansSection";
import { Portrait } from "./Portrait";

const PlansPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <PlansSection />
      <Comparative />
      <CardsSection />
      <Portrait />
    </React.Fragment>
  );
};

export { PlansPage };
