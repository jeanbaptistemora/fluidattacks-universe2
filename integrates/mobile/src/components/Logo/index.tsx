import React from "react";
import { View } from "react-native";
import type { SvgProps } from "react-native-svg";
import { SvgCss } from "react-native-svg";

import { styles } from "./styles";

import LogoSVG from "../../../assets/logo.svg";

const Logo: React.FC<SvgProps> = (props: SvgProps): JSX.Element => {
  return (
    <React.StrictMode>
      {/* Needed to override default styles */}
      {/* eslint-disable-next-line react/forbid-component-props */}
      <View style={styles.container} testID={"logo"}>
        {/* Needed in order to pass down props to SvgCss. */}
        {/* eslint-disable-next-line react/jsx-props-no-spreading*/}
        <SvgCss xml={LogoSVG} {...props} />
      </View>
    </React.StrictMode>
  );
};

export { Logo };
