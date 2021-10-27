// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { useTranslation } from "react-i18next";
import {
  Modal,
  Pressable,
  Text,
  View,
  useWindowDimensions,
} from "react-native";
import { useTheme } from "react-native-paper";

import { styles } from "./styles";

import Data from "../../../assets/licenses_data.json";
import { LicensesList } from "../LicensesList";
import type { ILicenseItem } from "../LicensesList/types";

const licensesJson: ILicenseItem[] = Object.keys(Data).map(
  (key: string): ILicenseItem => {
    // eslint-disable-next-line fp/no-rest-parameters
    const { licenses, ...license } = Data[key as keyof typeof Data];
    const lastIndex = key.lastIndexOf("@");
    const name = key.substr(0, lastIndex);
    const version = key.substr(lastIndex + 1);

    return {
      key,
      licenses,
      name,
      version,
      // eslint-disable-next-line fp/no-rest-parameters
      ...license,
    };
  }
);

interface ILicenses {
  visible: boolean;
  setVisible: (newValue: boolean) => void;
}

export const Licenses: React.FC<ILicenses> = ({
  visible,
  setVisible,
}: ILicenses): JSX.Element => {
  const { height, width } = useWindowDimensions();
  const { colors } = useTheme();
  const { t } = useTranslation();

  function changeModalVisibility(): void {
    setVisible(false);
  }

  return (
    <React.StrictMode>
      <Modal
        animationType={"slide"}
        onDismiss={changeModalVisibility}
        onRequestClose={changeModalVisibility}
        transparent={true}
        visible={visible}
      >
        <View
          style={{
            ...styles.modalView,
            backgroundColor: colors.background,
            maxHeight: height,
            maxWidth: width,
          }}
        >
          <View style={styles.buttonContainer}>
            <Text style={{ ...styles.text, color: colors.text }}>
              {t("about.licenses.title")}
            </Text>
            <Pressable onPress={changeModalVisibility} style={styles.button}>
              <Text
                style={{ ...styles.text, color: "#757575", fontWeight: "500" }}
              >
                {t("about.licenses.btn")}
              </Text>
            </Pressable>
          </View>
          <View style={styles.container}>
            <LicensesList licenses={licensesJson} />
          </View>
        </View>
      </Modal>
    </React.StrictMode>
  );
};
