import { default as Constants } from "expo-constants";
import * as Notifications from "expo-notifications";
import * as Permissions from "expo-permissions";
import { Platform } from "react-native";

const getToken: (() => Promise<string>) = async (
): Promise<string> => {
  const { data } = await Notifications.getExpoPushTokenAsync();

  if (Platform.OS === "android") {
    await Notifications.setNotificationChannelAsync("default", {
      importance: Notifications.AndroidImportance.MAX,
      lightColor: "#fe3435",
      name: "Integrates notifications",
    });
  }

  return data;
};

export const getPushToken: (() => Promise<string>) = async (
): Promise<string> => {
  /**
   * Push notifications are not supported on emulators
   *
   * @see https://docs.expo.io/versions/latest/sdk/notifications/#features
   */
  if (Constants.isDevice) {
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

    return "";
  }

  return "";
};
