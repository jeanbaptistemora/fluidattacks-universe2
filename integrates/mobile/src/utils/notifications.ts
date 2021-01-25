import { default as Constants } from "expo-constants";
import * as Notifications from "expo-notifications";
import * as Permissions from "expo-permissions";
import { Platform } from "react-native";

import { LOGGER } from "./logger";

const getToken: () => Promise<string> = async (): Promise<string> => {
  const token: Notifications.ExpoPushToken = await Notifications.getExpoPushTokenAsync();

  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelGroupAsync("default", {
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
      const { status: currentStatus } = await Permissions.getAsync(
        Permissions.NOTIFICATIONS,
      );

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
