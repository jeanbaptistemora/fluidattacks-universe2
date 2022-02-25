import React from "react";
import { Helmet } from "react-helmet";

import { ClientsSection } from "./ClientsSection";
import { ContactSection } from "./ContactSection";
import { NumbersSection } from "./NumbersSection";
import { Portrait } from "./Portrait";
import { ResourcesSection } from "./ResourcesSection";
import { ServiceSection } from "./ServiceSection";
import { SolutionsSection } from "./SolutionsSection";

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
    <NumbersSection />
    <SolutionsSection />
    <ResourcesSection />
    <ContactSection />
  </React.Fragment>
);

export { Home };
