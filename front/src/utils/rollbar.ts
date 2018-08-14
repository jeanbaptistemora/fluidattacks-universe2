import Rollbar from "rollbar";

const getEnvironment: (() => string) = (): string => {
  let environment: string;
  const currentUrl: string = window.location.href;
  if (currentUrl.indexOf("localhost:8000") !== -1) {
    environment = "development";
  } else if (currentUrl.indexOf(".integrates.env") !== -1) {
    environment = "review";
  } else if (currentUrl.indexOf("https://fluidattacks.com/") !== -1) {
    environment = "production";
  } else {
    throw new TypeError(`Couldn't identify environment for url: ${currentUrl}`);
  }

  return environment;
};

const config: Rollbar.Configuration = {
    accessToken: "cad6d1f7ecda480ba003e29f0428d44e",
    captureUncaught: true,
    captureUnhandledRejections: true,
    enabled: true,
    environment: getEnvironment(),
};

const rollbar: Rollbar = new Rollbar(config);

export = rollbar;
