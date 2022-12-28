import React, { createElement } from "react";
import { render } from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { ChartsForGroupView } from "scenes/Dashboard/containers/Group-Content/ChartsForGroupView";
import { GlobalStyle } from "styles";
import { secureStore, secureStoreContext } from "utils/secureStore";

const App: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <GlobalStyle />
    <BrowserRouter basename={"/graphics-for-group"}>
      <secureStoreContext.Provider value={secureStore}>
        <Switch>
          <Route component={ChartsForGroupView} path={"/"} />
        </Switch>
      </secureStoreContext.Provider>
    </BrowserRouter>
  </React.StrictMode>
);

render(createElement(App), document.getElementById("root"));
