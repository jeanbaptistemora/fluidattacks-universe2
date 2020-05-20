import * as SecureStore from "expo-secure-store";
import React from "react";
import { useTranslation } from "react-i18next";
import { Animated, View } from "react-native";
import { Drawer } from "react-native-paper";
import { useHistory } from "react-router-native";

import { Logo } from "../../../components/Logo";

import { styles } from "./styles";

/** Drawer menu */
interface ISidebarProps {
  progressAnimatedValue?: Animated.Value;
}

const sidebar: React.FunctionComponent<ISidebarProps> = (): JSX.Element => {
  const { t } = useTranslation();
  const history: ReturnType<typeof useHistory> = useHistory();

  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  return (
    <View style={styles.container}>
      <Logo width={180} height={50} fill="#FFFFFF" />
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

export const renderSidebar: ((progressAnimatedValue: Animated.Value) => JSX.Element) = (
  progressAnimatedValue: Animated.Value,
): JSX.Element => React.createElement(sidebar, { progressAnimatedValue });

export { sidebar as Sidebar };
