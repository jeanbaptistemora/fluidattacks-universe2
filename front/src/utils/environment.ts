import _ from "lodash";
import rollbar from "./rollbar";

export const getEnvironment: () => string = (): string => {
  if (_.isUndefined(window)) {
    return "development";
  } else {
    const currentUrl: string = window.location.hostname;

    if (currentUrl === "localhost") {
      return "development";
    } else if (_.includes(currentUrl, ".integrates.env")) {
      return "review";
    } else if (currentUrl === "fluidattacks.com") {
      return "production";
    } else {
      rollbar.error(
        "Couldn't identify environment for url",
        new TypeError(`Couldn't identify environment for url: ${currentUrl}`)
      );

      return "production";
    }
  }
};
