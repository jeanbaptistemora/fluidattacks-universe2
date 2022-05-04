import React from "react";
import { Helmet } from "react-helmet";

import { AboutUsSection } from "./AboutUsSection";
import { ClientsSection } from "./ClientsSection";
import { ContactSection } from "./ContactSection";
import { EbookSection } from "./EbookSection";
import { QualitySection } from "./QualitySection";
import { SolutionsSection } from "./SolutionsSection";

const Home: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Helmet>
      <meta
        content={"8hgdyewoknahd41nv3q5miuxx6sazj"}
        name={"facebook-domain-verification"}
      />
    </Helmet>
    <AboutUsSection />
    <SolutionsSection />
    <EbookSection />
    <ClientsSection />
    <ContactSection />
    <QualitySection />
  </React.Fragment>
);

export { Home };
