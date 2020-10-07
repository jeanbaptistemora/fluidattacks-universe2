import { ChartsForPortfolioView } from "scenes/Dashboard/containers/ChartsForPortfolioView";
import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter, Route, Switch } from "react-router-dom";
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

ReactDOM.render(React.createElement(App), document.getElementById("root"));
