import { Notifications } from "expo";
import { default as Constants } from "expo-constants";
import * as Permissions from "expo-permissions";
import { Platform } from "react-native";

import { LOGGER } from "./logger";

const getToken: (() => Promise<string>) = async (
): Promise<string> => {
  const token: string = await Notifications.getExpoPushTokenAsync();

  if (Platform.OS === "android") {
    await Notifications.createChannelAndroidAsync("default", {
      name: "Integrates notifications",
      priority: "max",
    });
  }

  return token;
};

export const getPushToken: (() => Promise<string>) = async (
): Promise<string> => {
  /**
   * Push notifications are not supported on emulators
   *
   * @see https://docs.expo.io/versions/latest/sdk/notifications/#features
   */
  if (Constants.isDevice) {
    try {
      const {
        status: currentStatus,
      } = await Permissions.getAsync(Permissions.NOTIFICATIONS);

      if (currentStatus === Permissions.PermissionStatus.GRANTED) {
        return getToken();
      }

      const { status } = await Permissions.askAsync(Permissions.NOTIFICATIONS);

      if (status === Permissions.PermissionStatus.GRANTED) {
        return getToken();
      }
    } catch (error) {
      LOGGER.error("Couldn't get push token", error);
    }

    return "";
  }

  return "";
};
