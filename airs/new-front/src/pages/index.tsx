import { Link, RouteComponentProps, Router } from "@reach/router";
import React from "react";
// tslint:disable-next-line: no-import-side-effect
import "tachyons/css/tachyons.min.css";

import { NavbarComponent } from "../components/navbar";
// tslint:disable-next-line: no-import-side-effect
import "../styles/index.scss";

// tslint:disable-next-line: variable-name
const Index: React.FC = (): JSX.Element => {

  return(
    <React.StrictMode>
      <div id="main">
        <NavbarComponent />
        <Router>
        </Router>
      </div>
    </React.StrictMode>
  );
};

export default Index;
