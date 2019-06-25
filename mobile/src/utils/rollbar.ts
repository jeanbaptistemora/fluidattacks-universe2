// tslint:disable-next-line: no-submodule-imports
import Rollbar from "rollbar/src/react-native/rollbar";

import { ROLLBAR_KEY } from "./constants";
import { getEnvironment } from "./context";

const config: Rollbar.Configuration = {
  accessToken: ROLLBAR_KEY,
  captureUncaught: true,
  captureUnhandledRejections: true,
  enabled: true,
  environment: `mobile-${getEnvironment().name}`,
};

export const rollbar: Rollbar = new Rollbar(config);
