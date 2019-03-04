import mixpanel from "mixpanel-browser";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import store from "../../store/index";
import { FindingContent } from "./containers/FindingContent";

const dashboardView: React.SFC = (): JSX.Element => (
  <React.StrictMode>
    <BrowserRouter basename={"/integrates/dashboard#!"}>
      <React.Fragment>
        <Provider store={store}>
          <Switch>
            <Route path="/project/:projectName/:findingId(\d+)/(\w+)" component={FindingContent} />
          </Switch>
        </Provider>
      </React.Fragment>
    </BrowserRouter>
  </React.StrictMode>
);

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
ReactDOM.render(React.createElement(dashboardView), document.getElementById("root"));
