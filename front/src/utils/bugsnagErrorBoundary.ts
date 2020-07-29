import Bugsnag from "@bugsnag/js";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import { OnErrorCallback } from "@bugsnag/core";
import React from "react";
import _ from "lodash";
import { getEnvironment } from "./environment";

type BugsnagErrorBoundary = React.ComponentType<{
  FallbackComponent?: React.ComponentType<{
    error: Error;
    info: React.ErrorInfo;
    clearError: () => void;
  }>;
  onError?: OnErrorCallback;
}>;

interface IBugsnagPluginReactResultConfig {
  createErrorBoundary: (react?: typeof React) => BugsnagErrorBoundary;
}

Bugsnag.start({
  apiKey: "99a64555a50340cfa856f6623c6bf35d",
  appVersion: "integrates_version",
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: getEnvironment(),
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
