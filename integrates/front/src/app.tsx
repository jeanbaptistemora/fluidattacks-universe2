import { MatomoProvider, createInstance } from "@datapunt/matomo-tracker-react";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useState } from "react";
import { render } from "react-dom";
import { useTranslation } from "react-i18next";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";

import { Announce } from "components/Announce";
import { MatomoWrapper } from "components/MatomoWrapper";
import { Dashboard } from "scenes/Dashboard";
import { Login } from "scenes/Login";
import { ApolloProvider } from "utils/apollo";
import { authContext } from "utils/auth";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "utils/authz/config";
import { BugsnagErrorBoundary } from "utils/bugsnagErrorBoundary";
import { getEnvironment } from "utils/environment";
import { useWindowSize } from "utils/hooks";
import { secureStore, secureStoreContext } from "utils/secureStore";
import "react-toastify/dist/ReactToastify.min.css";
import "tachyons/css/tachyons.min.css";
import "tachyons-word-break/css/tachyons-word-break.min.css";

const App: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const [user, setUser] = useState({
    tours: {
      newGroup: false,
      newOrganization: false,
      newRoot: false,
    },
    userEmail: "",
    userName: "",
  });
  const matomoInstance = createInstance({
    siteId: 3,
    urlBase: "https://fluidattacks.matomo.cloud",
  });
  const isProduction = getEnvironment() === "production";

  // Restrict small screens while we improve the responsive layout
  const { width } = useWindowSize();
  const minimumWidthAllowed = 768;
  if (width < minimumWidthAllowed) {
    return <Announce message={t("app.minimumWidth")} />;
  }

  return (
    <React.StrictMode>
      <MatomoProvider value={matomoInstance}>
        <BugsnagErrorBoundary>
          <BrowserRouter basename={"/"}>
            <MatomoWrapper enabled={isProduction}>
              <ApolloProvider>
                <authzPermissionsContext.Provider value={userLevelPermissions}>
                  <secureStoreContext.Provider value={secureStore}>
                    <authContext.Provider value={{ ...user, setUser }}>
                      <Switch>
                        <Route component={Login} exact={true} path={"/"} />
                        <Route component={Dashboard} path={"/"} />
                      </Switch>
                    </authContext.Provider>
                  </secureStoreContext.Provider>
                </authzPermissionsContext.Provider>
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

/**
 * Enable Hot Module Replacement for local development
 * @link https://webpack.js.org/concepts/hot-module-replacement/
 */
if (module.hot) {
  module.hot.accept();
}

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
if (getEnvironment() !== "production") {
  mixpanel.disable();
}

render(<App />, document.getElementById("root"));
