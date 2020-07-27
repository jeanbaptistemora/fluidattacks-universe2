import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import { Appbar, Text, useTheme } from "react-native-paper";

import { Avatar } from "../../../components/Avatar";
import { IUser } from "../../../utils/socialAuth";

import { styles } from "./styles";

/** App header */
interface IHeaderProps {
  user: IUser;
  onLogout(): void;
}

const header: React.FC<IHeaderProps> = (props: IHeaderProps): JSX.Element => {
  const { user, onLogout } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.avatar}>
          <Avatar
            photoUrl={user.photoUrl}
            size={40}
            userName={user.fullName}
          />
        </View>
        <Appbar.Content
          title={`${t("dashboard.greetingText")} ${user.firstName}`}
          titleStyle={styles.name}
          subtitle={user.email}
          subtitleStyle={styles.email}
        />
        <View style={styles.actions}>
          <Text style={styles.logout} onPress={onLogout}>
            {t("common.logout")}
          </Text>
        </View>
      </View>
    </React.StrictMode>
  );
};

export { header as Header };
