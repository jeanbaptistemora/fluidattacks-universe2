import { useMutation } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, View } from "react-native";
import { Text, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { Avatar } from "../../components/Avatar";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";
import { IAuthState, logout } from "../../utils/socialAuth";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import { ISignInResult } from "./types";

const welcomeView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const {
    authProvider, authToken, user,
  } = history.location.state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();

  const handleLogout: (() => void) = async (): Promise<void> => {
    await logout();
    history.replace("/Login");
  };

  // GraphQL operations
  const [signIn, { loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: async (result: ISignInResult): Promise<void> => {
      if (result.signIn.success) {
        await SecureStore.setItemAsync(
          "integrates_session",
          result.signIn.sessionJwt);
        history.replace("/Dashboard", { user });
      } else {
        rollbar.error("Unsuccessful API auth", result);
        Alert.alert(t("common.error.title"), t("common.error.msg"));
        handleLogout();
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
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.profilePicture}>
          <Avatar
            photoUrl={user.photoUrl}
            size={100} userName={user.fullName}
          />
        </View>
        <Text accessibilityStates="" style={styles.greeting} >
          {t("welcome.greetingText")} {user.firstName}!
           </Text>
        <Preloader visible={loading} />
      </View>
    </React.StrictMode>
  );
};

export { welcomeView as WelcomeView };
