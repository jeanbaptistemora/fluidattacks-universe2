import _ from "lodash";

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
      return "production";
    }
  }
};
