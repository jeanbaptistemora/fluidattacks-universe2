import type { Event } from "@bugsnag/core";
import Bugsnag from "@bugsnag/expo";
import BugsnagPluginReact from "@bugsnag/plugin-react";
import type {
  BugsnagErrorBoundary,
  BugsnagPluginReactResult,
} from "@bugsnag/plugin-react";
import type { NetworkState } from "expo-network";
import {
  getIpAddressAsync,
  getNetworkStateAsync,
  isAirplaneModeEnabledAsync,
} from "expo-network";
import _ from "lodash";
import React, { Fragment } from "react";
import { Platform } from "react-native";

import { BUGSNAG_KEY } from "./constants";
import { getEnvironment } from "./environment";
import { LOGGER } from "./logger";

Bugsnag.start({
  apiKey: BUGSNAG_KEY,
  onError: (event: Event): boolean => {
    // eslint-disable-next-line fp/no-mutation
    event.groupingHash = event.errors[0].errorMessage;

    return true;
  },
  plugins: [new BugsnagPluginReact(React)],
  releaseStage: `mobile-${getEnvironment().name}`,
});

const isAirplaneModeEnabled: () => Promise<boolean> = async (): Promise<boolean> =>
  Platform.OS === "android" ? isAirplaneModeEnabledAsync() : false;

Promise.all([getIpAddressAsync(), getNetworkStateAsync()])
  .then(
    async (networkInfo: [string, NetworkState]): Promise<void> => {
      Bugsnag.addMetadata("network", {
        IpAddress: networkInfo[0],
        IsAirplaneModeEnabled: await isAirplaneModeEnabled(),
        NetworkState: networkInfo[1],
      });
    }
  )
  .catch((error: Error): void => {
    LOGGER.error("Couldn't get network info", error);
  });

const reactPlugin: BugsnagPluginReactResult = Bugsnag.getPlugin(
  "react"
) as BugsnagPluginReactResult;

const bugsnagErrorBoundary: BugsnagErrorBoundary = _.isUndefined(reactPlugin)
  ? Fragment
  : reactPlugin.createErrorBoundary(React);

export { bugsnagErrorBoundary as BugsnagErrorBoundary };
