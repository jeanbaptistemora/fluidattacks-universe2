import React from "react";
import { Button, Image, View } from "react-native";
import { RouteComponentProps } from "react-router-native";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../assets/logo.png";

import { styles } from "./styles";

type ILoginProps = RouteComponentProps;

const loginView: React.FunctionComponent<ILoginProps> = (props: ILoginProps): JSX.Element => {
  const handleGoogleButtonClick: (() => void) = (): void => { props.history.push("/Menu"); };

  return (
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
      <View style={styles.buttonsContainer}>
        <Button title="Log in with Google" onPress={handleGoogleButtonClick} />
      </View>
    </View>
  );
};

export { loginView as LoginView };
