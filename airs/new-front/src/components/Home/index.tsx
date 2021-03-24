import { AboutUsSection } from "./AboutUsSection";
import { Portrait } from "./Portrait";
import React from "react";
import { VideoSection } from "./VideoSection";

const Home: React.FC = (): JSX.Element => (
  <React.Fragment>
    <Portrait />
    <VideoSection />
    <AboutUsSection />
  </React.Fragment>
);

export { Home };
