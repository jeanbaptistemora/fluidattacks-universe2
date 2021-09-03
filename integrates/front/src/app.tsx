import { MatomoProvider, createInstance } from "@datapunt/matomo-tracker-react";
import {
  disable as mixpanelDisable,
  init as mixpanelInit,
} from "mixpanel-browser";
import React, { createElement, useState } from "react";
import { render } from "react-dom";
import { Provider as ReduxProvider } from "react-redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import { MatomoWrapper } from "components/MatomoWrapper";
import { Dashboard } from "scenes/Dashboard";
import { Login } from "scenes/Login";
import store from "store";
import { ApolloProvider } from "utils/apollo";
import { authContext } from "utils/auth";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "utils/authz/config";
import { BugsnagErrorBoundary } from "utils/bugsnagErrorBoundary";
import { getEnvironment } from "utils/environment";
import { secureStore, secureStoreContext } from "utils/secureStore";
import "react-toastify/dist/ReactToastify.min.css";
import "tachyons/css/tachyons.min.css";
import "tachyons-word-break/css/tachyons-word-break.min.css";

const App: React.FC = (): JSX.Element => {
  const [user, setUser] = useState({ userEmail: "", userName: "" });
  const matomoInstance = createInstance({
    siteId: 3,
    urlBase: "https://fluidattacks.matomo.cloud",
  });
  const isProduction = getEnvironment() === "production";

  return (
    <React.StrictMode>
      <MatomoProvider value={matomoInstance}>
        <BugsnagErrorBoundary>
          <BrowserRouter basename={"/"}>
            <MatomoWrapper enabled={isProduction}>
              <ApolloProvider>
                <ReduxProvider store={store}>
                  <authzPermissionsContext.Provider
                    value={userLevelPermissions}
                  >
                    <secureStoreContext.Provider value={secureStore}>
                      <authContext.Provider value={{ ...user, setUser }}>
                        <Switch>
                          <Route component={Login} exact={true} path={"/"} />
                          <Route component={Dashboard} path={"/"} />
                        </Switch>
                      </authContext.Provider>
                    </secureStoreContext.Provider>
                  </authzPermissionsContext.Provider>
                </ReduxProvider>
              </ApolloProvider>
            </MatomoWrapper>
          </BrowserRouter>
          <ToastContainer
            autoClose={5000}
            closeOnClick={false}
            hideProgressBar={true}
            position={"top-right"}
          />
        </BugsnagErrorBoundary>
      </MatomoProvider>
    </React.StrictMode>
  );
};

const extendedModule: NodeModule & {
  hot?: { accept: () => void };
} = module as NodeModule & {
  hot?: { accept: () => void };
};
if (extendedModule.hot !== undefined) {
  extendedModule.hot.accept();
}

mixpanelInit("7a7ceb75ff1eed29f976310933d1cc3e");
if (getEnvironment() !== "production") {
  mixpanelDisable();
}

render(createElement(App), document.getElementById("root"));
