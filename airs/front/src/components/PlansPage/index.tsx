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
