import * as LocalAuthentication from "expo-local-authentication";
import * as SecureStore from "expo-secure-store";
import React from "react";
import { useTranslation } from "react-i18next";
import { Image, View } from "react-native";
import { Button, Headline, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as FluidIcon } from "../../../assets/notification.png";

import { styles } from "./styles";

const lockView: React.FC = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();

  // Side effects
  const promptBiometricAuth: (() => void) = async (): Promise<void> => {
    const authState: string =
      await SecureStore.getItemAsync("authState") as string;
    const { success } = await LocalAuthentication.authenticateAsync();

    if (success) {
      history.replace("/Dashboard", JSON.parse(authState));
    }
  };

  const onMount: (() => void) = (): void => {
    promptBiometricAuth();
  };

  React.useEffect(onMount, []);

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Image source={FluidIcon} style={styles.icon} />
      <Headline>{t("lock.title")}</Headline>
      <Button accessibilityStates="" mode="text" onPress={promptBiometricAuth}>
        {t("lock.btn")}
      </Button>
    </View>
  );
};

export { lockView as LockView };
