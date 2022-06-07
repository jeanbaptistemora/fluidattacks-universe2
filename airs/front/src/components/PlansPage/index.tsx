import React from "react";

import { Comparative } from "./Comparative ";
import { PlansSection } from "./PlansSection";

const PlansPage: React.FC = (): JSX.Element => {
  return (
    <React.Fragment>
      <PlansSection />
      <Comparative />
    </React.Fragment>
  );
};

export { PlansPage };
