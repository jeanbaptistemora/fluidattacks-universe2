import * as SecureStore from "expo-secure-store";
import React from "react";
import { useTranslation } from "react-i18next";
import { Animated, Image, View } from "react-native";
import { Drawer } from "react-native-paper";
import { useHistory } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../../assets/logo.png";

import { styles } from "./styles";

const sidebar: React.FunctionComponent<Animated.Value> = (): JSX.Element => {
  const { t } = useTranslation();
  const history: ReturnType<typeof useHistory> = useHistory();

  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  return (
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
      <View style={styles.bottom}>
        <Drawer.Item
          theme={{ colors: { text: "white" } }}
          icon="exit-to-app"
          label={t("common.logout")}
          onPress={handleLogout}
        />
      </View>
    </View>
  );
};

const renderSidebar: ((progressAnimatedValue: Animated.Value) => JSX.Element) = (
  progressAnimatedValue: Animated.Value,
): JSX.Element => React.createElement(sidebar, progressAnimatedValue);

export { renderSidebar as Sidebar };
