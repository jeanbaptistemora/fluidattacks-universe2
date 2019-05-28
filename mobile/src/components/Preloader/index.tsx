import React from "react";
import { Image, View } from "react-native";

// tslint:disable-next-line: no-default-import
import { default as loadingGif } from "../../../assets/loading.gif";

import { styles } from "./styles";

/**
 * Preloader component props
 */
interface IPreloaderProps {
  visible?: boolean;
}

const preloader: React.FC<IPreloaderProps> = (props: IPreloaderProps): JSX.Element => (
  <View style={styles.container}>
    {props.visible === true ? <Image source={loadingGif} style={styles.loadingGif} /> : undefined}
  </View>
);

preloader.defaultProps = {
  visible: true,
};

export { preloader as Preloader };
