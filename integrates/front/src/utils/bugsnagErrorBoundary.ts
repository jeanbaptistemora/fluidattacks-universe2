import Bugsnag from "@bugsnag/js";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import { Error } from "@bugsnag/core/types/event";
import React from "react";
import _ from "lodash";
import { getEnvironment } from "utils/environment";
import { Event, OnErrorCallback } from "@bugsnag/core";

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

const { userEmail, userName } = window as typeof window & Dictionary<string>;

Bugsnag.start({
  apiKey: "99a64555a50340cfa856f6623c6bf35d",
  appVersion: "integrates_version",
  onError: (event: Event): boolean => {
    event.errors.forEach((error: Error): void => {
      const message: string | undefined = event.context;
      // eslint-disable-next-line fp/no-mutation
      event.context = error.errorMessage;
      // eslint-disable-next-line fp/no-mutation
      error.errorMessage = _.isString(message) ? message : "";
      // eslint-disable-next-line fp/no-mutation
      event.groupingHash = event.context;
    });

    return true;
  },
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: getEnvironment(),
  user: {
    email: userEmail,
    name: userName,
  },
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
