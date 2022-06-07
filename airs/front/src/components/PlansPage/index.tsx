import React from "react";

import { CardsSection } from "./CardsSection";
import { Comparative } from "./Comparative ";
import { PlansSection } from "./PlansSection";

const PlansPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <PlansSection />
      <Comparative />
      <CardsSection />
    </React.Fragment>
  );
};

export { PlansPage };
