import Rollbar from "rollbar";
import { getEnvironment } from "./context";

const config: Rollbar.Configuration = {
    accessToken: "cad6d1f7ecda480ba003e29f0428d44e",
    captureUncaught: true,
    captureUnhandledRejections: true,
    enabled: true,
    environment: getEnvironment(),
    payload: {
        person: {
            id: (window as Window & { userEmail: string }).userEmail,
            username: (window as Window & { userName: string }).userName,
        },
    },
};

const rollbar: Rollbar = new Rollbar(config);

export = rollbar;
