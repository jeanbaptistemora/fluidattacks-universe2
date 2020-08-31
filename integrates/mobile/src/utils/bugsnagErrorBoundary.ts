import { Event, OnErrorCallback } from "@bugsnag/core";
import Bugsnag from "@bugsnag/expo";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import * as Network from "expo-network";
import _ from "lodash";
import React from "react";

import { BUGSNAG_KEY } from "./constants";
import { getEnvironment } from "./environment";
import { LOGGER } from "./logger";

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

Bugsnag.start({
  apiKey: BUGSNAG_KEY,
  onError: (event: Event): boolean => {
    event.groupingHash = event.errors[0].errorMessage;

    return true;
  },
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: `mobile-${getEnvironment().name}`,
});

Promise.all([
  Network.getIpAddressAsync(),
  Network.getNetworkStateAsync(),
  Network.isAirplaneModeEnabledAsync(),
])
  .then((networkInfo: [string, Network.NetworkState, boolean]): void => {
    Bugsnag.addMetadata("network", {
      IpAddress: networkInfo[0],
      IsAirplaneModeEnabled: networkInfo[2],
      NetworkState: networkInfo[1],
    });
  })
  .catch((error: Error): void => {
    LOGGER.error("Couldn't get network info", error);
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
