import Rollbar from "rollbar";

const getEnvironment: (() => string) = (): string => {
  let environment: string;
  /* tslint:disable-next-line:strict-type-predicates
   * Disabling this rule is necessary because the following expression is
   * misbelived to be always true by the linter while it is necessary for
   * avoiding errors in the npm test environment where the object window
   * doesn't exist.
   */
  if (typeof window === "undefined") {
    environment = "development";
  } else {
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
