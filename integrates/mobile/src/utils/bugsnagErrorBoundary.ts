import { Event } from "@bugsnag/core";
import Bugsnag from "@bugsnag/expo";
import BugsnagPluginReact, {
  BugsnagErrorBoundary,
  BugsnagPluginReactResult,
} from "@bugsnag/plugin-react";
import * as Network from "expo-network";
import _ from "lodash";
import React from "react";

import { BUGSNAG_KEY } from "./constants";
import { getEnvironment } from "./environment";
import { LOGGER } from "./logger";

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

const reactPlugin: BugsnagPluginReactResult =
  Bugsnag.getPlugin("react") as BugsnagPluginReactResult;

const bugsnagErrorBoundary: BugsnagErrorBoundary = _.isUndefined(reactPlugin)
  ? React.Fragment
  : reactPlugin.createErrorBoundary(React);

export { bugsnagErrorBoundary as BugsnagErrorBoundary };
