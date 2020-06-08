import { AndroidManifest, default as Constants } from "expo-constants";
import _ from "lodash";

import { rollbar } from "../../utils/rollbar";

export const checkPlayStoreVersion: (() => Promise<boolean>) = async (): Promise<boolean> => {
  let isOutdated: boolean = false;

  const androidManifest: AndroidManifest = Constants.manifest.android as AndroidManifest;
  const response: Response = await fetch(`https://play.google.com/store/apps/details?id=${androidManifest.package}`);
  const html: string = await response.text();
  const match: RegExpMatchArray | null = html.match(/>[0-9]+\.?[0-9]+\.?[0-9]+</);

  if (_.isNull(match)) {
    rollbar.error("Couldn't retrieve play store version", html);
  } else {
    const remoteVersion: string = match[0].slice(1, -1);
    const localVersion: string = String(Constants.nativeAppVersion);
    isOutdated = remoteVersion.localeCompare(localVersion) !== 0;
  }

  return isOutdated;
};
