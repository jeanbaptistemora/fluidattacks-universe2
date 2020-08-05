import { OnErrorCallback } from "@bugsnag/core";
import Bugsnag from "@bugsnag/expo";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import { default as Constants } from "expo-constants";
import _ from "lodash";
import React from "react";

import { BUGSNAG_KEY } from "./constants";
import { getEnvironment } from "./environment";

type BugsnagErrorBoundary = React.ComponentType<{
  FallbackComponent?: React.ComponentType<{
    error: Error;
    info: React.ErrorInfo;
    clearError(): void;
  }>;
  onError?: OnErrorCallback;
}>;

/**
 * Bugsnag react plugin type
 */
interface IBugsnagPluginReactResultConfig {
  createErrorBoundary(react?: typeof React): BugsnagErrorBoundary;
}

const appVersion: string = _.isString(Constants.nativeAppVersion)
  ? Constants.nativeAppVersion
  : "";

Bugsnag.start({
  apiKey: BUGSNAG_KEY,
  appVersion,
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: `mobile-${getEnvironment().name}`,

});

const reactPlugin:
  | IBugsnagPluginReactResultConfig
  | undefined = Bugsnag.getPlugin("react");

const bugsnagErrorBoundary:
  | BugsnagErrorBoundary
  | React.ExoticComponent = _.isUndefined(reactPlugin)
  ? React.Fragment
  : reactPlugin.createErrorBoundary(React);

export { bugsnagErrorBoundary as BugsnagErrorBoundary };
