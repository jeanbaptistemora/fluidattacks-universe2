import React from "react";
import { Text, View } from "react-native";
import { SvgCss, XmlProps } from "react-native-svg";

// tslint:disable-next-line: no-default-import
import { default as Logo } from "../../../assets/logo.svg";

import { styles } from "./styles";

type LogoProps = Omit<XmlProps, "xml">;

const logo: React.FC<LogoProps> = (props: LogoProps): JSX.Element => (
  <React.StrictMode>
    <View style={styles.container}>
      <SvgCss xml={Logo} {...props} />
      <Text style={{ color: (props.fill as string | undefined) }}>
        by Fluid Attacks
      </Text>
    </View>
  </React.StrictMode>
);

export { logo as Logo };
