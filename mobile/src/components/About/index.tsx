import { MaterialIcons } from "@expo/vector-icons";
import { default as Constants } from "expo-constants";
import * as Updates from "expo-updates";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, View } from "react-native";
import { Text } from "react-native-paper";

import { styles } from "./styles";

const about: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  const displayDialog: (() => void) = (): void => {
    Alert.alert(
      "Integrates",
      `v.${Constants.manifest.version}`
      + `\nOTA v.${(Updates.manifest as Updates.Manifest).version}`,
    );
  };

  return (
    <View style={styles.container}>
      <MaterialIcons name="info-outline" size={14} color="#808080" />
      <Text style={styles.text} accessibilityStates="" onPress={displayDialog}>
        {t("common.about")}
      </Text>
    </View>
  );
};

export { about as About };
