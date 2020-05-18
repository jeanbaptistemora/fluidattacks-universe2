import React from "react";
import { Animated, Image, View } from "react-native";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../../assets/logo.png";

import { styles } from "./styles";

const sidebar: React.FunctionComponent<Animated.Value> = (): JSX.Element => (
  <React.StrictMode>
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
    </View>
  </React.StrictMode>
);

const renderSidebar: ((progressAnimatedValue: Animated.Value) => JSX.Element) = (
  progressAnimatedValue: Animated.Value,
): JSX.Element => React.createElement(sidebar, progressAnimatedValue);

export { renderSidebar as Sidebar };
