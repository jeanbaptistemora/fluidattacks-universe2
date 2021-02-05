import { default as Constants } from "expo-constants";

/**
 * Environment data
 */
interface IEnvironment {
  name: string;
  url: string;
}

export const getEnvironment: () => IEnvironment = (): IEnvironment => {
  const { hostUri, releaseChannel } = Constants.manifest;

  if (__DEV__ || releaseChannel === "local") {
    const hostAddress: string = (hostUri as string).split(":")[0];

    return {
      name: "development",
      url: `http://${hostAddress}:8001`,
    };
  }

  if ((releaseChannel as string).endsWith("atfluid")) {
    return {
      name: "ephemeral",
      url: `https://${releaseChannel}.integrates.fluidattacks.com`,
    };
  }

  if (releaseChannel === "master") {
    return {
      name: "production",
      url: "https://integrates.fluidattacks.com",
    };
  }

  throw new TypeError("Couldn't identify environment");
};
