import { default as Constants } from "expo-constants";
import * as Device from "expo-device";
import * as Updates from "expo-updates";
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
    app: {
      version: {
        binary: Constants.nativeAppVersion,
        ota: (Updates.manifest as Updates.Manifest).version,
      },
    },
    device: {
      brand: Device.brand,
      manufacturer: Device.manufacturer,
      model: Device.modelName,
      name: Device.designName,
      os: {
        name: Device.osName,
        version: Device.osVersion,
      },
      product: Device.productName,
    },
  },
  platform: Platform.OS,
};

export const rollbar: Rollbar = new Rollbar(config);
