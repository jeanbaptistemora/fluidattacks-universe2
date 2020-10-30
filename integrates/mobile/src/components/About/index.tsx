import { MaterialIcons } from "@expo/vector-icons";
import { default as Constants } from "expo-constants";
import * as Updates from "expo-updates";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, Linking, View } from "react-native";

import { styles } from "./styles";

const manifest: Updates.Manifest = Updates.manifest as Updates.Manifest;
const manifestExtra: Record<string, string> = manifest.extra === undefined
  ? {
      commitSha: "",
      commitShaShort: "",
      deploymentDate: "",
    }
  : manifest.extra as Record<string, string>;

const about: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const displayDialog: (() => void) = (): void => {
    Alert.alert(
      "Integrates",
      `${t("about.bin")} ${Constants.nativeAppVersion}`
      + `\n${t("about.deploymentDate")} ${manifestExtra.deploymentDate}`
      + `\n${t("about.commit")} ${manifestExtra.commitShaShort}`,
      [
        {
          onPress: (): Promise<string> => Linking.openURL(
            `https://gitlab.com/fluidattacks/product/-/tree/${manifestExtra.commitSha}`,
          ),
          text: "Commit Details",
        },
        { text: "Ok" },
      ],
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
