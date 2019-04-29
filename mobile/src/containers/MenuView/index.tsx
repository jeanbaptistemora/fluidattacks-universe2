import React from "react";
import { Text, View } from "react-native";
import { styles } from "./styles";

const menuView: React.FunctionComponent = (): JSX.Element => (
  <View style={styles.container}>
    <Text>Hello world</Text>
  </View>
);

export { menuView as MenuView };
