import { Constants } from "expo";
import { Platform } from "react-native";

export const checkVersion: (() => Promise<boolean>) = async (): Promise<boolean> => new Promise((
  resolve: ((isOutdated: boolean) => void), reject: ((error: Error) => void),
): void => {
  if (Platform.OS === "android") {
    const androidManifest: typeof Constants.manifest["android"] =
      Constants.manifest.android === undefined ? {} : Constants.manifest.android;

    fetch(`https://play.google.com/store/apps/details?id=${androidManifest.package}`)
      .then((httpResponse: Response) => httpResponse.text())
      .then((rawHTML: string): void => {
        const match: RegExpMatchArray | null = rawHTML.match(/>[0-9]+\.?[0-9]+\.?[0-9]+</);
        if (match !== null) {
          const remoteVersion: string = match[0].slice(1, -1);
          const localVersion: string = String(Constants.manifest.version);
          resolve(remoteVersion.localeCompare(localVersion) > 0);
        }
      })
      .catch((error: Error): void => { reject(error); });
  }
});
