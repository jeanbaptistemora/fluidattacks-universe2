import Rollbar from "rollbar";
import { getEnvironment } from "./environment";

const { userEmail, userName } = window as typeof window & Dictionary<string>;

const config: Rollbar.Configuration = {
    accessToken: "cad6d1f7ecda480ba003e29f0428d44e",
    captureUncaught: true,
    captureUnhandledRejections: true,
    enabled: getEnvironment() !== "development",
    environment: getEnvironment(),
    payload: {
        person: {
            id: userEmail,
            username: userName,
        },
    },
};

const rollbar: Rollbar = new Rollbar(config);

export = rollbar;
