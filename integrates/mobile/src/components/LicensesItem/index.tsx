// Needed to override styles
/* eslint-disable react/forbid-component-props */
import React from "react";
import { Linking, Text, TouchableOpacity, View } from "react-native";
import { useTheme } from "react-native-paper";

import { styles } from "./styles";

import { Link } from "../Link";

interface ILicensesItem {
  licenses: string;
  licenseUrl: string;
  name: string;
  repository: string;
  version: string;
}

export const LicensesItem: React.FC<ILicensesItem> = ({
  licenses,
  licenseUrl,
  name,
  repository,
  version,
}: ILicensesItem): JSX.Element => {
  const { colors } = useTheme();

  async function handlePress(): Promise<void> {
    await Linking.openURL(repository);
  }

  return (
    <View>
      <View style={styles.cardShadow}>
        <View style={styles.card}>
          <TouchableOpacity onPress={handlePress} style={styles.item}>
            <View>
              <Text style={{ ...styles.name, color: colors.text }}>{name}</Text>
              <Text style={{ ...styles.text, color: colors.text }}>
                {version}
              </Text>
              <Link
                style={{
                  ...styles.text,
                  color: "lightblue",
                  textDecorationLine: "underline",
                }}
                url={licenseUrl}
              >
                {licenses}
              </Link>
            </View>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
};
