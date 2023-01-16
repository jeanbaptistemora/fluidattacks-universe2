import React from "react";
import { Helmet } from "react-helmet";

import { ClientsSection } from "./ClientsSection";
import { ContinuousCycle } from "./ContinuousCycle";
import { DiscoverContinuous } from "./DiscoverContinuous";
import { HeaderHero } from "./HeaderHero";
import { HomeCta } from "./HomeCta";
import { Reviews } from "./ReviewsSection";
import { SolutionsSection } from "./SolutionsSection";

const HomePage: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Helmet>
      <meta
        content={"8hgdyewoknahd41nv3q5miuxx6sazj"}
        name={"facebook-domain-verification"}
      />
    </Helmet>
    <HeaderHero />
    <ClientsSection
      sectionColor={"#25252d"}
      titleColor={"#f4f4f6"}
      titleSize={"24"}
    />
    <DiscoverContinuous />
    <ContinuousCycle />
    <SolutionsSection />
    <Reviews />
    <HomeCta />
  </React.Fragment>
);

export { HomePage };
