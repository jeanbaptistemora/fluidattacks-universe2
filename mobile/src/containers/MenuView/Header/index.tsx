import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { View } from "react-native";
import { Avatar, Text, useTheme } from "react-native-paper";

import { styles } from "./styles";

/** App header */
interface IHeaderProps {
  photoUrl?: string;
  userName?: string;
  onLogout(): void;
}

const header: React.FC<IHeaderProps> = (props: IHeaderProps): JSX.Element => {
  const { onLogout } = props;
  const { colors } = useTheme();
  const { t } = useTranslation();

  const maxInitials: number = 2;
  const getInitials: ((name: string) => string) = (name: string): string => name
    .split(" ")
    .splice(0, maxInitials)
    .map((word: string): string => word
      .charAt(0)
      .toUpperCase())
    .join("");

  const fullName: string = _.get(props, "userName", "");

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.avatar}>
          {props.photoUrl === undefined
            ? <Avatar.Text size={40} label={getInitials(fullName)} />
            : <Avatar.Image size={40} source={{ uri: props.photoUrl }} />}
        </View>
        <Text style={styles.greeting}>{t("menu.greetingText")} {fullName.split(" ")[0]}</Text>
        <View style={styles.actions}>
          <Text style={styles.logout} onPress={onLogout}>{t("common.logout")}</Text>
        </View>
      </View>
    </React.StrictMode>
  );
};

export { header as Header };
