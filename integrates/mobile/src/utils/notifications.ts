// eslint-disable-next-line import/no-named-as-default -- Needed for accessing isDevice correctly
import Constants from "expo-constants";
import type { ExpoPushToken } from "expo-notifications";
import {
  getExpoPushTokenAsync,
  getPermissionsAsync,
  requestPermissionsAsync,
  setNotificationChannelGroupAsync,
} from "expo-notifications";
import { Platform } from "react-native";

import { LOGGER } from "./logger";

const getToken: () => Promise<string> = async (): Promise<string> => {
  const token: ExpoPushToken = await getExpoPushTokenAsync();

  if (Platform.OS === "android") {
    await setNotificationChannelGroupAsync("default", {
      name: "Integrates notifications",
    });
  }

  return token.data;
};

export const getPushToken: () => Promise<string> = async (): Promise<string> => {
  /**
   * Push notifications are not supported on emulators
   *
   * @see https://docs.expo.io/versions/latest/sdk/notifications/#features
   */
  if (Constants.isDevice) {
    try {
      const { status: currentStatus } = await getPermissionsAsync();

      if (currentStatus === "granted") {
        return await getToken();
      }

      const { status } = await requestPermissionsAsync();

      if (status === "granted") {
        return await getToken();
      }
    } catch (error: unknown) {
      LOGGER.error("Couldn't get push token", error);
    }

    return "";
  }

  return "";
};
