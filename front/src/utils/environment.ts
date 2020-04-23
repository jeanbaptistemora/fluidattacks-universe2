import _ from "lodash";

export const getEnvironment: (() => string) = (): string => {
  let environment: string;

  if (_.isUndefined(window)) {
    environment = "development";
  } else {
    const currentUrl: string = window.location.hostname;

    if (currentUrl === "localhost") {
      environment = "development";
    } else if (_.includes(currentUrl, ".integrates.env")) {
      environment = "review";
    } else if (currentUrl === "fluidattacks.com") {
      environment = "production";
    } else {
      throw new TypeError(`Couldn't identify environment for url: ${currentUrl}`);
    }
  }

  return environment;
};
