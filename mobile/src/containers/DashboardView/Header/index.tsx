import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import { Text, useTheme } from "react-native-paper";

import { Avatar } from "../../../components/Avatar";

import { styles } from "./styles";

/** App header */
interface IHeaderProps {
  photoUrl?: string;
  userName: string;
  onLogout(): void;
}

const header: React.FC<IHeaderProps> = (props: IHeaderProps): JSX.Element => {
  const { onLogout } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.avatar}>
          <Avatar photoUrl={props.photoUrl} size={40} userName={props.userName} />
        </View>
        <Text style={styles.greeting}>{t("dashboard.greetingText")} {props.userName.split(" ")[0]}</Text>
        <View style={styles.actions}>
          <Text style={styles.logout} onPress={onLogout}>{t("common.logout")}</Text>
        </View>
      </View>
    </React.StrictMode>
  );
};

export { header as Header };
