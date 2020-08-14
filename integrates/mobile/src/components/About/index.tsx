import { MaterialIcons } from "@expo/vector-icons";
import { default as Constants } from "expo-constants";
import * as Updates from "expo-updates";
import React from "react";
import { Alert, View } from "react-native";

import { styles } from "./styles";

const about: React.FC = (): JSX.Element => {
  const displayDialog: (() => void) = (): void => {
    Alert.alert(
      "Integrates",
      `BIN v.${Constants.nativeAppVersion}`
      + `\nOTA v.${(Updates.manifest as Updates.Manifest).version}`,
    );
  };

  return (
    <View style={styles.container}>
      <MaterialIcons
        color="#808080"
        name="info-outline"
        onPress={displayDialog}
        size={15}
      />
    </View>
  );
};

export { about as About };
