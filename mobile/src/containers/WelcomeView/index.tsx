import React from "react";
import { Image, Text, View } from "react-native";
import { RouteComponentProps } from "react-router-native";

import { translate } from "../../utils/translations/translate";
import { ILoginState } from "../LoginView/reducer";

import { styles } from "./styles";

type IWelcomeProps = RouteComponentProps<{}, {}, { userInfo: ILoginState["userInfo"] }>;

const welcomeView: React.FunctionComponent<IWelcomeProps> = (props: IWelcomeProps): JSX.Element => {
  const { userInfo } = props.location.state;
  const { t } = translate;

  const delayBeforeTransition: number = 2500;
  setTimeout((): void => { props.history.push("/Menu"); }, delayBeforeTransition);

  return (
    <View style={styles.container}>
      <Image style={styles.profilePicture} source={{ uri: userInfo.photoUrl }} />
      <Text style={styles.greeting}>{t("welcome.greetingText")} {userInfo.givenName}!</Text>
    </View>
  );
};

export { welcomeView as WelcomeView };
