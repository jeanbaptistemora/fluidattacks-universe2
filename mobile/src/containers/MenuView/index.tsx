import React from "react";
import { Text, View } from "react-native";
import { RouteComponentProps } from "react-router-native";

import { translate } from "../../utils/translations/translate";

import { styles } from "./styles";

type IMenuProps = RouteComponentProps;

const menuView: React.FunctionComponent<IMenuProps> = (): JSX.Element => {
  const { t } = translate;

  return (
    <View style={styles.container}>
      <Text>{t("menu.myProjects")}</Text>
    </View>
  );
};

export { menuView as MenuView };
