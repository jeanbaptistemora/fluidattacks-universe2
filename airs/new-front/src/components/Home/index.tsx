import { AboutUsSection } from "./AboutUsSection";
import { ClientsSection } from "./ClientsSection";
import { ContactSection } from "./ContactSection";
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
    <ContactSection />
  </React.Fragment>
);

export { Home };
