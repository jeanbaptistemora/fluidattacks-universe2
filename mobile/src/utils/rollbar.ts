import * as Device from "expo-device";
import { Platform } from "react-native";
// tslint:disable-next-line: no-submodule-imports
import Rollbar from "rollbar/src/react-native/rollbar";

import { ROLLBAR_KEY } from "./constants";
import { getEnvironment } from "./environment";

const config: Rollbar.Configuration = {
  accessToken: ROLLBAR_KEY,
  captureUncaught: true,
  captureUnhandledRejections: true,
  enabled: getEnvironment().name !== "development",
  environment: `mobile-${getEnvironment().name}`,
  payload: {
    os: {
      android_version: Device.osVersion,
      brand: Device.brand,
      device: Device.designName,
      manufacturer: Device.manufacturer,
      os: Device.osName,
      phone_model: Device.modelName,
      product: Device.productName,
    },
  },
  platform: Platform.OS,
};

export const rollbar: Rollbar = new Rollbar(config);
