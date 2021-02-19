import { Layout } from "../components/layout";
import { NavbarComponent } from "../components/navbar";
import React from "react";

import "tachyons/css/tachyons.min.css";
import "../styles/index.scss";

const Index: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <Layout>
      <NavbarComponent />
    </Layout>
  </React.StrictMode>
);

// eslint-disable-next-line import/no-default-export
export default Index;
