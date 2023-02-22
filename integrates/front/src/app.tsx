import { MatomoProvider, createInstance } from "@datapunt/matomo-tracker-react";
import "@fontsource/roboto";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useMemo, useState } from "react";
import { render } from "react-dom";
import { useTranslation } from "react-i18next";
import { BrowserRouter, Route, Switch } from "react-router-dom";

import { GlobalStyle } from "./styles";

import { ToastBox } from "components/Alert";
import { Announce } from "components/Announce";
import { MatomoWrapper } from "components/MatomoWrapper";
import { Login } from "scenes/Login";
import { SignUp } from "scenes/SignUp";
import { Welcome } from "scenes/Welcome";
import { ApolloProvider } from "utils/apollo";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "utils/authz/config";
import { BugsnagErrorBoundary } from "utils/bugsnagErrorBoundary";
import { getEnvironment } from "utils/environment";
import type { IFeaturePreviewContext } from "utils/featurePreview";
import { featurePreviewContext } from "utils/featurePreview";
import { useStoredState, useWindowSize } from "utils/hooks";
import { secureStore, secureStoreContext } from "utils/secureStore";
import "react-toastify/dist/ReactToastify.min.css";
import "tachyons/css/tachyons.min.css";
import "tachyons-word-break/css/tachyons-word-break.min.css";

const App: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const [user, setUser] = useState({
    tours: {
      newGroup: true,
      newRiskExposure: true,
      newRoot: true,
      welcome: true,
    },
    userEmail: "",
    userName: "",
  });
  const [featurePreview, setFeaturePreview] = useStoredState(
    "featurePreview",
    false,
    localStorage
  );

  const matomoInstance = createInstance({
    siteId: 3,
    urlBase: "https://fluidattacks.matomo.cloud",
  });
  const isProduction = getEnvironment() === "production";

  const valueAuth = useMemo((): IAuthContext => ({ ...user, setUser }), [user]);

  const valueFeature = useMemo(
    (): IFeaturePreviewContext => ({ featurePreview, setFeaturePreview }),
    [featurePreview, setFeaturePreview]
  );

  // Restrict small screens while we improve the responsive layout
  const { width } = useWindowSize();
  const minimumWidthAllowed = 768;
  if (width < minimumWidthAllowed) {
    return (
      <React.Fragment>
        <GlobalStyle />
        <Announce message={t("app.minimumWidth")} />
      </React.Fragment>
    );
  }

  return (
    <React.StrictMode>
      <GlobalStyle />
      <MatomoProvider value={matomoInstance}>
        <BugsnagErrorBoundary>
          <BrowserRouter basename={"/"}>
            <MatomoWrapper enabled={isProduction}>
              <ApolloProvider>
                <authzPermissionsContext.Provider value={userLevelPermissions}>
                  <secureStoreContext.Provider value={secureStore}>
                    <authContext.Provider value={valueAuth}>
                      <featurePreviewContext.Provider value={valueFeature}>
                        <Switch>
                          <Route component={Login} exact={true} path={"/"} />
                          <Route component={SignUp} path={"/SignUp"} />
                          <Route component={Welcome} path={"/"} />
                        </Switch>
                      </featurePreviewContext.Provider>
                    </authContext.Provider>
                  </secureStoreContext.Provider>
                </authzPermissionsContext.Provider>
              </ApolloProvider>
            </MatomoWrapper>
          </BrowserRouter>
          <ToastBox autoClose={5000} position={"top-right"} />
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
