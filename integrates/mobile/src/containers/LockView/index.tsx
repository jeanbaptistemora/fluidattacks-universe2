// Needed to override styles
/* eslint-disable react/forbid-component-props */
import { authenticateAsync } from "expo-local-authentication";
import { getItemAsync } from "expo-secure-store";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Image, View } from "react-native";
import { Button, Headline, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { styles } from "./styles";

import FluidIcon from "../../../assets/notification.png";

const LockView: React.FC = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();

  // Side effects
  const promptBiometricAuth: () => void = async (): Promise<void> => {
    const authState: string = (await getItemAsync("authState")) as string;
    const { success } = await authenticateAsync();

    if (success) {
      history.replace("/Dashboard", JSON.parse(authState));
    }
  };

  const onMount: () => void = (): void => {
    promptBiometricAuth();
  };
  // We only want this to run when the component mounts.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(onMount, []);

  return (
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Image source={FluidIcon} style={styles.icon} />
      <Headline>{t("lock.title")}</Headline>
      <Button
        accessibilityComponentType={undefined}
        accessibilityTraits={undefined}
        mode={"text"}
        // eslint-disable-next-line react/jsx-no-bind -- Needed to allow auth
        onPress={promptBiometricAuth}
      >
        {t("lock.btn")}
      </Button>
    </View>
  );
};

export { LockView };
