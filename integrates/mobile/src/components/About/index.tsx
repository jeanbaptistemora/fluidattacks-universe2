import { MaterialIcons } from "@expo/vector-icons";
// eslint-disable-next-line import/no-named-as-default
import Constants from "expo-constants";
import type { Manifest } from "expo-updates";
import { manifest } from "expo-updates";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { Alert, Linking, View } from "react-native";

import { styles } from "./styles";

const manifestConst: Manifest = manifest as Manifest;
const manifestExtra: Record<string, string> =
  manifestConst.extra === undefined
    ? {
        commitSha: "",
        commitShaShort: "",
        deploymentDate: "",
      }
    : (manifestConst.extra as Record<string, string>);

const About: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const displayDialog: () => void = useCallback((): void => {
    Alert.alert(
      "Integrates",
      // eslint-disable-next-line @typescript-eslint/restrict-template-expressions
      `${t("about.bin")} ${Constants.nativeAppVersion}` +
        `\n${t("about.deploymentDate")} ${manifestExtra.deploymentDate}` +
        `\n${t("about.commit")} ${manifestExtra.commitShaShort}`,
      [
        {
          onPress: async (): Promise<string> =>
            // eslint-disable-next-line @typescript-eslint/no-unsafe-return
            Linking.openURL(
              `https://gitlab.com/fluidattacks/product/-/tree/${manifestExtra.commitSha}`
            ),
          text: "Commit Details",
        },
        { text: "Ok" },
      ]
    );
  }, [t]);

  return (
    // eslint-disable-next-line react/forbid-component-props
    <View style={styles.container}>
      <MaterialIcons
        color={"#808080"}
        name={"info-outline"}
        onPress={displayDialog}
        size={15}
      />
    </View>
  );
};

export { About };
