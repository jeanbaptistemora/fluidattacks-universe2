import Rollbar from "rollbar";
import { getEnvironment } from "./context";

const config: Rollbar.Configuration = {
    accessToken: "cad6d1f7ecda480ba003e29f0428d44e",
    captureUncaught: true,
    captureUnhandledRejections: true,
    enabled: true,
    environment: getEnvironment(),
};

const rollbar: Rollbar = new Rollbar(config);

export = rollbar;
