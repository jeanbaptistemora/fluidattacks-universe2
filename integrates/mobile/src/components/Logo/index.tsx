import LogoSVG from "../../../assets/logo.svg";
import React from "react";
import { SvgCss } from "react-native-svg";
import type { XmlProps } from "react-native-svg";
import { styles } from "./styles";
import { Text, View } from "react-native";

type LogoProps = Omit<XmlProps, "xml">;

const Logo: React.FC<LogoProps> = (props: LogoProps): JSX.Element => {
  const { fill } = props;

  return (
    <React.StrictMode>
      {/* Needed to override default styles */}
      {/* eslint-disable-next-line react/forbid-component-props */}
      <View style={styles.container}>
        {/* Needed in order to pass down props to SvgCss. */}
        {/* eslint-disable-next-line react/jsx-props-no-spreading*/}
        <SvgCss xml={LogoSVG} {...props} />
        {/* eslint-disable-next-line react/forbid-component-props*/}
        <Text style={{ color: fill as string | undefined }}>
          {"by Fluid Attacks"}
        </Text>
      </View>
    </React.StrictMode>
  );
};

export { Logo };
