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
};

export const rollbar: Rollbar = new Rollbar(config);
