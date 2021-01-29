import { Event } from "@bugsnag/core";
import Bugsnag from "@bugsnag/expo";
import BugsnagPluginReact, {
  BugsnagErrorBoundary,
  BugsnagPluginReactResult,
} from "@bugsnag/plugin-react";
import * as Network from "expo-network";
import _ from "lodash";
import React from "react";
import { Platform } from "react-native";

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

Promise.all([Network.getIpAddressAsync(), Network.getNetworkStateAsync()])
  .then(
    async (networkInfo: [string, Network.NetworkState]): Promise<void> => {
      const isAirplaneModeEnabled: boolean = Platform.select({
        android: await Network.isAirplaneModeEnabledAsync(),
        default: false,
      });

      Bugsnag.addMetadata("network", {
        IpAddress: networkInfo[0],
        IsAirplaneModeEnabled: isAirplaneModeEnabled,
        NetworkState: networkInfo[1],
      });
    },
  )
  .catch((error: Error): void => {
    LOGGER.error("Couldn't get network info", error);
  });

const reactPlugin: BugsnagPluginReactResult = Bugsnag.getPlugin(
  "react",
) as BugsnagPluginReactResult;

const bugsnagErrorBoundary: BugsnagErrorBoundary = _.isUndefined(reactPlugin)
  ? React.Fragment
  : reactPlugin.createErrorBoundary(React);

export { bugsnagErrorBoundary as BugsnagErrorBoundary };
