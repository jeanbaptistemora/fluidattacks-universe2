import mixpanel from "mixpanel-browser";
import React from "react";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { ScrollUpButton } from "../../components/ScrollUpButton";
import store from "../../store/index";
import Navbar from "./components/Navbar/index";
import {
  eventDescriptionView as EventDescriptionView, eventEvidenceView as EventEvidenceView,
} from "./containers/EventDescriptionView/index";
import FindingContent from "./containers/FindingContent/index";
import ProjectContent from "./containers/ProjectContent/index";

const dashboardView: React.SFC = (): JSX.Element => (
  <React.StrictMode>
    <BrowserRouter basename={"/integrates/dashboard#!"}>
      <React.Fragment>
        <Provider store={store}>
          <React.Fragment>
            <Navbar />
            <Switch>
              <Route
                path="/project/:projectName/events/:eventId(\d+)/description"
                exact={true}
                component={EventDescriptionView}
              />
              <Route
                path="/project/:projectName/events/:eventId(\d+)/evidence"
                exact={true}
                component={EventEvidenceView}
              />
              <Route path="/project/:projectName/(\w+)" exact={true} component={ProjectContent} />
              <Route path="/project/:projectName/:findingId(\d+)/(\w+)" component={FindingContent} />
            </Switch>
          </React.Fragment>
        </Provider>
      </React.Fragment>
    </BrowserRouter>
    <ScrollUpButton visibleAt={400} />
  </React.StrictMode>
);

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
ReactDOM.render(React.createElement(dashboardView), document.getElementById("root"));
