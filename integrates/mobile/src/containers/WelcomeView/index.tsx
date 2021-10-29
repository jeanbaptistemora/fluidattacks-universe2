import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import {
  SecurityLevel,
  getEnrolledLevelAsync,
} from "expo-local-authentication";
import { setItemAsync } from "expo-secure-store";
import React, { useEffect } from "react";
import { useTranslation } from "react-i18next";
import { Alert, View } from "react-native";
import { Text, useTheme } from "react-native-paper";
import { useHistory } from "react-router-native";

import { SIGN_IN_MUTATION } from "./queries";
import { styles } from "./styles";
import type { ISignInResult } from "./types";

import { Avatar } from "../../components/Avatar";
import { Preloader } from "../../components/Preloader";
import { LOGGER } from "../../utils/logger";
import { useSessionToken } from "../../utils/sessionToken/context";
import type { IAuthState } from "../../utils/socialAuth";
import { logout } from "../../utils/socialAuth";

const WelcomeView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { authProvider, authToken, user } = history.location
    .state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();
  const [, setSessionToken] = useSessionToken();

  const handleLogout: () => void = async (): Promise<void> => {
    await logout(setSessionToken);
    history.replace("/Login");
  };

  // GraphQL operations
  const [signIn, { loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: async (result: ISignInResult): Promise<void> => {
      if (result.signIn.success) {
        setSessionToken(result.signIn.sessionJwt);
        await getEnrolledLevelAsync().then(
          async (value: SecurityLevel): Promise<void> => {
            if (value === SecurityLevel.BIOMETRIC) {
              await setItemAsync("session_token", result.signIn.sessionJwt);
            }
          }
        );
        history.replace("/Dashboard", { user });
      } else {
        LOGGER.error("Unsuccessful API auth", result);
        Alert.alert(t("common.error.title"), t("common.error.msg"));
        handleLogout();
      }
    },
    onError: (error: ApolloError): void => {
      LOGGER.error("API auth failed", error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
      handleLogout();
    },
    variables: { authToken, provider: authProvider },
  });

  // Side effects
  const onMount: () => void = (): void => {
    const executeMutation: () => void = async (): Promise<void> => {
      await signIn();
    };
    executeMutation();
  };
  useEffect(onMount, [signIn]);

  return (
    <React.StrictMode>
      {/* eslint-disable-next-line react/forbid-component-props */}
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        {/* eslint-disable-next-line react/forbid-component-props */}
        <View style={styles.profilePicture}>
          <Avatar
            photoUrl={user.photoUrl}
            size={100}
            userName={user.fullName}
          />
        </View>
        <Text
          // eslint-disable-next-line react/forbid-component-props
          style={styles.greeting}
        >
          {t("welcome.greetingText")} {user.firstName}
          {"!"}
        </Text>
        <Preloader visible={loading} />
      </View>
    </React.StrictMode>
  );
};

export { WelcomeView };
