import _ from "lodash";

export const getEnvironment: () => string = (): string => {
  if (_.isUndefined(window)) {
    return "development";
  } else {
    const currentUrl: string = window.location.hostname;
    const ephemeralDomainRegex: RegExp = /[a-z]+atfluid.integrates.fluidattacks.com/gu;

    if (currentUrl === "localhost") {
      return "development";
    } else if (ephemeralDomainRegex.test(currentUrl)) {
      return "review";
    } else {
      return "production";
    }
  }
};
