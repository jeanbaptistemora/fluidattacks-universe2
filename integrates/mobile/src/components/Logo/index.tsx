import React from "react";
import { View } from "react-native";
import type { XmlProps } from "react-native-svg";
import { SvgCss } from "react-native-svg";

import { styles } from "./styles";

import LogoSVG from "../../../assets/new-logo.svg";

type LogoProps = Omit<XmlProps, "xml">;

const Logo: React.FC<LogoProps> = (props: LogoProps): JSX.Element => {
  return (
    <React.StrictMode>
      {/* Needed to override default styles */}
      {/* eslint-disable-next-line react/forbid-component-props */}
      <View style={styles.container}>
        {/* Needed in order to pass down props to SvgCss. */}
        {/* eslint-disable-next-line react/jsx-props-no-spreading*/}
        <SvgCss xml={LogoSVG} {...props} />
        {/* eslint-disable-next-line react/forbid-component-props*/}
      </View>
    </React.StrictMode>
  );
};

export { Logo };
