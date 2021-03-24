import { AboutUsSection } from "./AboutUsSection";
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
  </React.Fragment>
);

export { Home };
