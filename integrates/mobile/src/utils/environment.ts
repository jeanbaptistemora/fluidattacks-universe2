// eslint-disable-next-line import/no-named-default -- Needed for using manifest correctly
import { default as Constants } from "expo-constants";
import type { AppManifest } from "expo-constants/build/Constants.types";

/**
 * Environment data
 */
interface IEnvironment {
  name: string;
  url: string;
}

export const getEnvironment: () => IEnvironment = (): IEnvironment => {
  const { hostUri, releaseChannel } = Constants.manifest as AppManifest;

  if (__DEV__ || releaseChannel === "local") {
    const [hostAddress] = (hostUri as string).split(":");

    return {
      name: "development",
      url: `http://${hostAddress}:8001`,
    };
  }

  if ((releaseChannel as string).endsWith("atfluid")) {
    return {
      name: "ephemeral",
      url: `https://${releaseChannel as string}.app.fluidattacks.com`,
    };
  }

  if (releaseChannel === "master") {
    return {
      name: "production",
      url: "https://app.fluidattacks.com",
    };
  }

  // eslint-disable-next-line fp/no-throw
  throw new TypeError("Couldn't identify environment");
};
