import LogRocket from "logrocket";
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
  // Type object on payload comes from Rollbar.Configuration["transform"].
  // eslint-disable-next-line @typescript-eslint/ban-types
  transform: (payload: object): Record<string, unknown> => ({
    ...payload,
    sessionURL: LogRocket.sessionURL,
  }),
};

const rollbar: Rollbar = new Rollbar(config);

export default rollbar;
