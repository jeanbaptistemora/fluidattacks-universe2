import { Notifications } from "expo";
import * as Permissions from "expo-permissions";

export const getPushToken: (() => Promise<string>) = async (): Promise<string> => {
  let notifPermission: Permissions.PermissionStatus;
  notifPermission = (await Permissions.getAsync(Permissions.NOTIFICATIONS)).status;

  if (notifPermission !== Permissions.PermissionStatus.GRANTED) {
    notifPermission = (await Permissions.askAsync(Permissions.NOTIFICATIONS)).status;
  }

  return notifPermission === Permissions.PermissionStatus.GRANTED
    ? Notifications.getExpoPushTokenAsync()
    : "";
};
