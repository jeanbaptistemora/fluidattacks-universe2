// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

import "./static/scss/index.scss";
import "gatsby-plugin-breadcrumb/gatsby-plugin-breadcrumb.css";
import "animate.css/animate.min.css";
import "tachyons/css/tachyons.min.css";
import "highlight.js/styles/github.css";
import Bugsnag from "@bugsnag/js";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import _ from "lodash";
import React, { Fragment } from "react";
import { Auth0Provider } from "@auth0/auth0-react";
import { navigate } from "gatsby";

const getEnvironment = () => {
  if (_.isUndefined(window)) {
    return "development";
  }
  const currentUrl = window.location.hostname;
  const ephemeralDomainRegex = /^web.eph.fluidattacks.com/gu;

  if (currentUrl === "localhost") {
    return "development";
  } else if (ephemeralDomainRegex.test(currentUrl)) {
    return "ephemeral";
  }

  return "production";
};

Bugsnag.start({
  apiKey: "6d0d7e66955855de59cfff659e6edf31",
  appVersion: "airs_version",
  onError: (event) => {
    event.errors.forEach((error) => {
      const message = event.context;
      event.context = error.errorMessage;
      error.errorMessage = _.isString(message) ? message : "";
      event.groupingHash = event.context;
    });

    return true;
  },
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: getEnvironment(),
});

const reactPlugin = Bugsnag.getPlugin("react");

const BugsnagErrorBoundary = _.isUndefined(reactPlugin)
  ? Fragment
  : reactPlugin.createErrorBoundary(React);

const onRedirectCallback = (appState) => {
  navigate(appState?.returnTo || "/", { replace: true });
};

export const wrapRootElement = ({ element }) => (
  <Auth0Provider
    domain={process.env.AUTH0_DOMAIN}
    clientId={process.env.AUTH0_CLIENT_ID}
    redirectUri={window.location.origin}
    onRedirectCallback={onRedirectCallback}
  >
    <BugsnagErrorBoundary>{element}</BugsnagErrorBoundary>
  </Auth0Provider>
);
