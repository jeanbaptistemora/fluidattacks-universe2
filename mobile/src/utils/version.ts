import { AndroidManifest, default as Constants } from "expo-constants";
import _ from "lodash";
import { Platform } from "react-native";

export const checkVersion: (() => Promise<boolean>) = async (): Promise<boolean> => new Promise((
  resolve: ((isOutdated: boolean) => void), reject: ((error: Error) => void),
): void => {
  if (Platform.OS === "android") {
    const androidManifest: AndroidManifest = Constants.manifest.android as AndroidManifest;

    fetch(`https://play.google.com/store/apps/details?id=${androidManifest.package}`)
      .then((httpResponse: Response): Promise<string> => httpResponse.text())
      .then((rawHTML: string): void => {
        const match: RegExpMatchArray | null = rawHTML.match(/>[0-9]+\.?[0-9]+\.?[0-9]+</);
        if (!_.isNull(match)) {
          const remoteVersion: string = match[0].slice(1, -1);
          const localVersion: string = String(Constants.manifest.version);
          resolve(remoteVersion.localeCompare(localVersion) > 0);
        } else {
          reject(new Error("Couldn't retrieve remoteVersion: Invalid package name"));
        }
      })
      .catch((error: Error): void => { reject(error); });
  } else {
    resolve(true);
  }
});
