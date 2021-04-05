// Needed to override default styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import { Appbar, Text, useTheme } from "react-native-paper";

import { styles } from "./styles";

import { Avatar } from "../../../components/Avatar";
import type { IUser } from "../../../utils/socialAuth";

/** App header */
interface IHeaderProps {
  user: IUser;
  onLogout: () => void;
}

const Header: React.FC<IHeaderProps> = (props: IHeaderProps): JSX.Element => {
  const { user, onLogout } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.avatar}>
          <Avatar photoUrl={user.photoUrl} size={40} userName={user.fullName} />
        </View>
        <Appbar.Content
          accessibilityComponentType={undefined}
          accessibilityTraits={undefined}
          color={colors.text}
          subtitle={user.email}
          subtitleStyle={styles.email}
          title={user.fullName}
          titleStyle={styles.name}
        />
        <View style={styles.actions}>
          <Text
            accessibilityComponentType={undefined}
            accessibilityTraits={undefined}
            onPress={onLogout}
            style={styles.logout}
          >
            {t("common.logout")}
          </Text>
        </View>
      </View>
    </React.StrictMode>
  );
};

export { Header };
