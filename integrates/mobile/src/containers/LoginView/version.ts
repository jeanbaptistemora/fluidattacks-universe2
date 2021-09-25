// Needed for correct usage of AndroidManifest
import Constants from "expo-constants"; // eslint-disable-line import/no-named-as-default
import type { AndroidManifest } from "expo-constants";
import { Platform } from "react-native";

import { LOGGER } from "../../utils/logger";

const getVersionFromPlaystore: () => Promise<string> =
  async (): Promise<string> => {
    const androidManifest: AndroidManifest = Constants.manifest
      ?.android as AndroidManifest;

    const baseURL: string = "https://play.google.com/store/apps/details";
    const response: Response = await fetch(
      `${baseURL}?id=${androidManifest.package as string}`
    );

    if (response.ok) {
      const html: string = await response.text();
      const index: number = html.search("Current Version");
      const startOffset: number = 81;
      const endOffset: number = 92;

      return html.substring(index + startOffset, index + endOffset);
    }
    // Needed for the test
    // eslint-disable-next-line fp/no-throw
    throw Error(`Received HTTP status ${response.status}`);
  };

export const getOutdatedStatus: () => Promise<boolean> =
  async (): Promise<boolean> => {
    const localVersion: string = String(Constants.nativeAppVersion);
    try {
      const remoteVersion: string = Platform.select({
        android: await getVersionFromPlaystore(),
        default: localVersion,
      });

      return localVersion !== remoteVersion;
    } catch (error: unknown) {
      LOGGER.warning("Couldn't retrieve remote version", error);

      return false;
    }
  };
