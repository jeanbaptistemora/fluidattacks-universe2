import React from "react";
import { Helmet } from "react-helmet";

import { ClientsSection } from "./ClientsSection";
import { Portrait } from "./Portrait";
import { ServiceSection } from "./ServiceSection";

const Home: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Helmet>
      <meta
        content={"8hgdyewoknahd41nv3q5miuxx6sazj"}
        name={"facebook-domain-verification"}
      />
    </Helmet>
    <Portrait />
    <ClientsSection />
    <ServiceSection />
  </React.Fragment>
);

export { Home };
