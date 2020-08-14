import { ChartsForOrganizationView } from "../../scenes/Dashboard/containers/ChartsForOrganizationView";
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { secureStore, secureStoreContext } from "../../utils/secureStore/index";

const App: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <BrowserRouter basename={"/integrates/graphics-for-organization"}>
      <secureStoreContext.Provider value={secureStore}>
        <Switch>
          <Route component={ChartsForOrganizationView} path={"/"} />
        </Switch>
      </secureStoreContext.Provider>
    </BrowserRouter>
  </React.StrictMode>
);

ReactDOM.render(React.createElement(App), document.getElementById("root"));
