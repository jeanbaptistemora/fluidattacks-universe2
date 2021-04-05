import React from "react";

import { AboutUsSection } from "./AboutUsSection";
import { ClientsSection } from "./ClientsSection";
import { ContactSection } from "./ContactSection";
import { EbookSection } from "./EbookSection";
import { Portrait } from "./Portrait";
import { QualitySection } from "./QualitySection";
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
    <QualitySection />
  </React.Fragment>
);

export { Home };
