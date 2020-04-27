import { default as Constants } from "expo-constants";
import _ from "lodash";

/**
 * Environment data
 */
interface IEnvironment {
  name: string;
  url: string;
}

export const getEnvironment: (() => IEnvironment) = (): IEnvironment => {
  const { releaseChannel } = Constants.manifest;

  let environment: IEnvironment;
  if (__DEV__ || releaseChannel === "local") {
    environment = {
      name: "development",
      url: `http://${String(Constants.manifest.hostUri)
        .split(":")[0]}:8080`,
    };
  } else if (releaseChannel === "master") {
    environment = { name: "production", url: "https://fluidattacks.com" };
  } else if (_.endsWith(String(releaseChannel), "atfluid")) {
    environment = { name: "review", url: `https://${releaseChannel}.integrates.env.fluidattacks.com` };
  } else {
    throw new TypeError("Couldn't identify environment");
  }

  return environment;
};
