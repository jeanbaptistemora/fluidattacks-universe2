// eslint-disable-next-line import/no-named-as-default -- Needed for accessing isDevice correctly
import Constants from "expo-constants";
import type { ExpoPushToken } from "expo-notifications";
import { LOGGER } from "./logger";
import { Platform } from "react-native";
import {
  NOTIFICATIONS,
  PermissionStatus,
  askAsync,
  getAsync,
} from "expo-permissions";
import {
  getExpoPushTokenAsync,
  setNotificationChannelGroupAsync,
} from "expo-notifications";

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
      const { status: currentStatus } = await getAsync(NOTIFICATIONS);

      if (currentStatus === PermissionStatus.GRANTED) {
        return await getToken();
      }

      const { status } = await askAsync(NOTIFICATIONS);

      if (status === PermissionStatus.GRANTED) {
        return await getToken();
      }
    } catch (error: unknown) {
      LOGGER.error("Couldn't get push token", error);
    }

    return "";
  }

  return "";
};
