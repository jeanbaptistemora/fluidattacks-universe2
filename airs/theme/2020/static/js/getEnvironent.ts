import _ from "lodash";

let environment: string;
export const getEnvironment: () => string = (): string => {
  if (_.isUndefined(window)) {
    environment = "development";
  } else {
    const currentUrl: string = window.location.hostname;
    const ephemeralDomainRegex: RegExp = /^web.eph/gu;

    if (currentUrl === "localhost") {
      environment = "development";
    } else if (ephemeralDomainRegex.test(currentUrl)) {
      environment = "ephemeral";
    } else {
      environment = "production";
    }
  }

  return environment;
};
