import { AndroidManifest, default as Constants } from "expo-constants";
import _ from "lodash";
import { Platform } from "react-native";

import { LOGGER } from "../../utils/logger";

const getCommitFromPlaystore: () => Promise<string> = async (): Promise<string> => {
  const androidManifest: AndroidManifest = Constants.manifest
    .android as AndroidManifest;

  const baseURL: string = "https://play.google.com/store/apps/details";
  const response: Response = await fetch(
    `${baseURL}?id=${androidManifest.package}`,
  );

  if (response.ok) {
    const html: string = await response.text();

    // Find commit ref in playstore HTML
    const index: number = html.search("Current Version");
    const startOffset: number = 81;
    const endOffset: number = 88;

    return html.substring(index + startOffset, index + endOffset);
  }

  throw Error(`Received HTTP status ${response.status}`);
};

export const getOutdatedStatus: () => Promise<boolean> = async (): Promise<boolean> => {
  const localVersion: string = String(Constants.nativeAppVersion);
  try {
    const remoteVersion: string = Platform.select({
      android: await getCommitFromPlaystore(),
      default: localVersion,
    });

    return localVersion !== remoteVersion;
  } catch (error) {
    LOGGER.warning("Couldn't retrieve remote version", error);

    return false;
  }
};
