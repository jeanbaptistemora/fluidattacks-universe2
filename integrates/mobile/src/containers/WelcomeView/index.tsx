import type { ApolloError } from "@apollo/client";
import { Avatar } from "../../components/Avatar";
import type { IAuthState } from "../../utils/socialAuth";
import type { ISignInResult } from "./types";
import { LOGGER } from "../../utils/logger";
import { Preloader } from "../../components/Preloader";
import { SIGN_IN_MUTATION } from "./queries";
import { logout } from "../../utils/socialAuth";
import { setItemAsync } from "expo-secure-store";
import { styles } from "./styles";
import { useHistory } from "react-router-native";
import { useMutation } from "@apollo/client";
import { useTranslation } from "react-i18next";
import { Alert, View } from "react-native";
import React, { useEffect } from "react";
import { Text, useTheme } from "react-native-paper";

const WelcomeView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { authProvider, authToken, user } = history.location
    .state as IAuthState;
  const { colors } = useTheme();
  const { t } = useTranslation();

  const handleLogout: () => void = async (): Promise<void> => {
    await logout();
    history.replace("/Login");
  };

  // GraphQL operations
  const [signIn, { loading }] = useMutation(SIGN_IN_MUTATION, {
    onCompleted: async (result: ISignInResult): Promise<void> => {
      if (result.signIn.success) {
        await setItemAsync("integrates_session", result.signIn.sessionJwt);
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
          accessibilityComponentType={undefined}
          accessibilityTraits={undefined}
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
