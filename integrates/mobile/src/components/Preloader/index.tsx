import React from "react";
import loadingGif from "../../../assets/loading.gif";
import { styles } from "./styles";
import { Image, View } from "react-native";

/**
 * Preloader component props
 */
interface IPreloaderProps {
  visible: boolean;
}

const Preloader: React.FC<IPreloaderProps> = ({
  visible,
}: IPreloaderProps): JSX.Element => (
  // Needed to override default styles
  // eslint-disable-next-line react/forbid-component-props
  <View style={styles.container}>
    {visible ? (
      // eslint-disable-next-line react/forbid-component-props
      <Image source={loadingGif} style={styles.loadingGif} />
    ) : undefined}
  </View>
);

export { Preloader };
