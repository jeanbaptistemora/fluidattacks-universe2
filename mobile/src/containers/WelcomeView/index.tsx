import { useMutation } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, Image, Text, View } from "react-native";
import { Button } from "react-native-paper";
import { useHistory } from "react-router-native";

import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import { IAuthResult, ISignInResult } from "./types";

const welcomeView: React.FunctionComponent = (): JSX.Element => {
  const { t } = useTranslation();
  const history: ReturnType<typeof useHistory> = useHistory();
  const { authProvider, authToken, userInfo } = history.location.state as IAuthResult;

  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  // State management
  const [isAuthorized, setAuthorized] = React.useState(false);

  // GraphQL operations
  const [signIn, { loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: (result: ISignInResult): void => {
      if (result.signIn.success) {
        setAuthorized(result.signIn.authorized);
        SecureStore.setItemAsync("integrates_session", result.signIn.sessionJwt)
          .then((): void => {
            if (result.signIn.authorized) {
              history.replace("/Menu");
            }
          })
          .catch((error: Error): void => {
            rollbar.error("An error occurred storing JWT", error);
          });
      } else {
        rollbar.error("Unsuccessful API auth", result);
      }
    },
    onError: (error: ApolloError): void => {
      rollbar.error("API auth failed", error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
    },
    variables: { authToken, provider: authProvider },
  });

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
      {loading || isAuthorized ? undefined : (
        <React.Fragment>
          <Text style={styles.unauthorized}>{t("welcome.unauthorized")}</Text>
          <Button onPress={handleLogout}>{t("common.logout")}</Button>
        </React.Fragment>
      )}
      <Preloader visible={loading} />
    </View>
  );
};

export { welcomeView as WelcomeView };
