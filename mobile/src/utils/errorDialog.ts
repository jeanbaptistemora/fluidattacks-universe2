import { Alert, Platform, ToastAndroid } from "react-native";

import { translate } from "./translations/translate";

export const show: (() => void) = (): void => {
  const { t } = translate;

  switch (Platform.OS) {
    case "android":
      ToastAndroid.show(t("common.error"), ToastAndroid.SHORT);
      break;
    case "ios":
      Alert.alert("Error", t("common.error"));
      break;
    default:
    // Unsupported platform
  }
};
