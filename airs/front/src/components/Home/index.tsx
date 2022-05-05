import React from "react";
import { Helmet } from "react-helmet";

import { ContactSection } from "./ContactSection";
import { QualitySection } from "./QualitySection";

const Home: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Helmet>
      <meta
        content={"8hgdyewoknahd41nv3q5miuxx6sazj"}
        name={"facebook-domain-verification"}
      />
    </Helmet>
    <ContactSection />
    <QualitySection />
  </React.Fragment>
);

export { Home };
