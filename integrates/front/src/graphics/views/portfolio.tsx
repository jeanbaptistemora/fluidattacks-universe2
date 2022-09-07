/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React, { createElement } from "react";
import { render } from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import { secureStore, secureStoreContext } from "utils/secureStore";

const App: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <BrowserRouter basename={"/graphics-for-portfolio"}>
      <secureStoreContext.Provider value={secureStore}>
        <Switch>
          <Route component={ChartsForPortfolioView} path={"/"} />
        </Switch>
      </secureStoreContext.Provider>
    </BrowserRouter>
  </React.StrictMode>
);

render(createElement(App), document.getElementById("root"));
