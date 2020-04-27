/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code in graphql queries
 */

import { useMutation } from "@apollo/react-hooks";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { Image, Text, View } from "react-native";

import { Preloader } from "../../components/Preloader";
import * as errorDialog from "../../utils/errorDialog";
import { rollbar } from "../../utils/rollbar";
import { translate } from "../../utils/translations/translate";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import { ISignInResult, IWelcomeProps } from "./types";

const welcomeView: React.FunctionComponent<IWelcomeProps> = (props: IWelcomeProps): JSX.Element => {
  const { authProvider, authToken, pushToken, userInfo } = props.location.state;
  const { t } = translate;

  // GraphQL operations
  const [signIn, { data, loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: (result: ISignInResult): void => {
      if (result.signIn.success) {
        SecureStore.setItemAsync("integrates_session", result.signIn.sessionJwt)
          .then((): void => {
            if (result.signIn.authorized) {
              props.history.push("/Menu");
            }
          })
          .catch((error: Error): void => {
            rollbar.error("Error: An error occurred storing jwt", error);
          });
      } else {
        errorDialog.show();
      }
    },
    onError: (): void => {
      errorDialog.show();
    },
    variables: { authToken, provider: authProvider, pushToken },
  });

  const unauthorized: boolean = data !== undefined && !data.signIn.authorized;

  // Side effects
  const onMount: (() => void) = (): void => {
    const executeMutation: (() => void) = async (): Promise<void> => {
      await signIn();
    };
    executeMutation();
  };
  React.useEffect(onMount, []);

  return (
    <View style={styles.container}>
      <Image style={styles.profilePicture} source={{ uri: userInfo.photoUrl }} />
      <Text style={styles.greeting}>{t("welcome.greetingText")} {userInfo.givenName}!</Text>
      {loading ? <Preloader /> : undefined}
      {unauthorized ? <Text style={styles.unauthorized}>{t("welcome.unauthorized")}</Text> : undefined}
    </View>
  );
};

export { welcomeView as WelcomeView };
