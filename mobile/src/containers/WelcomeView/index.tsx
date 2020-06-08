import { useMutation } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, StatusBar, Text, View } from "react-native";
import { useHistory } from "react-router-native";

import { Avatar } from "../../components/Avatar";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import { IAuthState, ISignInResult } from "./types";

const welcomeView: React.FunctionComponent = (): JSX.Element => {
  const { t } = useTranslation();
  const history: ReturnType<typeof useHistory> = useHistory();
  const { authProvider, authToken, user } = history.location.state as IAuthState;

  const handleLogout: (() => void) = async (): Promise<void> => {
    await SecureStore.deleteItemAsync("integrates_session");
    history.replace("/");
  };

  // GraphQL operations
  const [signIn, { loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: async (result: ISignInResult): Promise<void> => {
      if (result.signIn.success) {
        try {
          await SecureStore.setItemAsync("integrates_session", result.signIn.sessionJwt);
          history.replace("/Dashboard", { user });
        } catch (error) {
          rollbar.error("An error occurred storing JWT", error as Error);
        }
      } else {
        rollbar.error("Unsuccessful API auth", result);
      }
    },
    onError: (error: ApolloError): void => {
      rollbar.error("API auth failed", error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
      handleLogout();
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
    <React.StrictMode>
      <StatusBar backgroundColor="transparent" barStyle="light-content" translucent={true} />
      <View style={styles.container}>
        <View style={styles.profilePicture}>
          <Avatar photoUrl={user.photoUrl} size={100} userName={user.fullName} />
        </View>
        <Text style={styles.greeting}>{t("welcome.greetingText")} {user.firstName}!</Text>
        <Preloader visible={loading} />
      </View>
    </React.StrictMode>
  );
};

export { welcomeView as WelcomeView };
