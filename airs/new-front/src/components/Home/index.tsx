import { AboutUsSection } from "./AboutUsSection";
import { ClientsSection } from "./ClientsSection";
import { EbookSection } from "./EbookSection";
import { Portrait } from "./Portrait";
import React from "react";
import { SolutionsSection } from "./SolutionsSection";
import { VideoSection } from "./VideoSection";

const Home: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Portrait />
    <VideoSection />
    <AboutUsSection />
    <SolutionsSection />
    <EbookSection />
    <ClientsSection />
  </React.Fragment>
);

export { Home };
