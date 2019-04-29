import React from "react";
import { Button, Image, View, ToastAndroid } from "react-native";
import { RouteComponentProps } from "react-router-native";
import { Google } from "expo";

// tslint:disable-next-line: no-default-import
import { default as FluidLogo } from "../../../assets/logo.png";

import { styles } from "./styles";

type ILoginProps = RouteComponentProps;

const loginView: React.FunctionComponent<ILoginProps> = (props: ILoginProps): JSX.Element => {
  const handleGoogleButtonClick: (() => void) = (): void => {
    Google.logInAsync({
      androidClientId: "335718398321-vv3cfdee0ng40tuhgm5g2mp42c2d2o9j.apps.googleusercontent.com",
      scopes: ["profile", "email"],
    }).then((result: Google.LogInResult) => {
      if (result.type === "success") {
        props.history.push("/Menu", { userInfo: result.user });
      }
    }).catch((e: Error) => {
      ToastAndroid.show('Oops! There is an error.', ToastAndroid.SHORT);
      throw e;
    });
  };

  return (
    <View style={styles.container}>
      <Image source={FluidLogo} style={styles.logo} />
      <View style={styles.buttonsContainer}>
        <Button title="Log in with Google" color="#cc0000" onPress={handleGoogleButtonClick} />
      </View>
    </View>
  );
};

export { loginView as LoginView };
