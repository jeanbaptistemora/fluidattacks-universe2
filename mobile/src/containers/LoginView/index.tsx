import { AppOwnership, default as Constants, NativeConstants } from "expo-constants";
import * as Google from "expo-google-app-auth";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Alert, Linking, Platform, StatusBar, View } from "react-native";
import { Button, Dialog, Paragraph, Portal, Text } from "react-native-paper";
import { useHistory } from "react-router-native";

import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import {
  GOOGLE_LOGIN_KEY_ANDROID_DEV,
  GOOGLE_LOGIN_KEY_ANDROID_PROD,
  GOOGLE_LOGIN_KEY_IOS_DEV,
  GOOGLE_LOGIN_KEY_IOS_PROD,
} from "../../utils/constants";
import { rollbar } from "../../utils/rollbar";
import { checkVersion } from "../../utils/version";

import { GoogleButton } from "./GoogleButton";
import { styles } from "./styles";

type manifestStructure = NativeConstants["manifest"] & { android: { package: string } };
const manifest: manifestStructure = (Constants.manifest as manifestStructure);

const loginView: React.FunctionComponent = (): JSX.Element => {
  const { t } = useTranslation();
  const history: ReturnType<typeof useHistory> = useHistory();

  // State management
  const [isLoading, setLoading] = React.useState(true);
  const [isOutdated, setOutdated] = React.useState(false);

  // Side effects
  const onMount: (() => void) = (): void => {
    const executeCheckVersion: (() => void) = async (): Promise<void> => {
      try {
        const shouldSkipCheck: boolean =
          Platform.OS === "ios"
          || Constants.appOwnership === AppOwnership.Expo;

        if (shouldSkipCheck) {
          setOutdated(false);
        } else {
          setOutdated(await checkVersion());
        }
      } catch (error) {
        rollbar.error("An error occurred getting latest version", error as Error);
      }
      setLoading(false);
    };

    executeCheckVersion();
  };
  React.useEffect(onMount, []);

  // Event handlers
  const handleGoogleButtonClick: (() => void) = async (): Promise<void> => {
    setLoading(true);
    try {
      const result: Google.LogInResult = await Google.logInAsync({
        androidClientId: GOOGLE_LOGIN_KEY_ANDROID_DEV,
        androidStandaloneAppClientId: GOOGLE_LOGIN_KEY_ANDROID_PROD,
        clientId: "",
        iosClientId: GOOGLE_LOGIN_KEY_IOS_DEV,
        iosStandaloneAppClientId: GOOGLE_LOGIN_KEY_IOS_PROD,
        scopes: ["profile", "email"],
      });
      if (result.type === "success") {
        history.replace("/Welcome", {
          authProvider: "google",
          authToken: String(result.idToken),
          userInfo: result.user,
        });
      } else {
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);
      rollbar.error("An error occurred authenticating with Google", error as Error);
      Alert.alert(t("common.error.title"), t("common.error.msg"));
    }
  };

  const handleUpdateButtonClick: (() => void) = async (): Promise<void> => {
    await Linking.openURL(`market://details?id=${manifest.android.package}`);
  };

  return (
    <React.StrictMode>
      <StatusBar backgroundColor="transparent" barStyle="light-content" translucent={true} />
      <View style={styles.container}>
        <Logo width={300} height={70} fill="#FFFFFF" />
        <View style={styles.buttonsContainer}>
          <GoogleButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleGoogleButtonClick}
          />
        </View>
        <Preloader visible={isLoading} />
        <View style={styles.bottom}>
          <Text style={styles.slogan}>{t("common.slogan")}</Text>
        </View>
        <Portal>
          <Dialog dismissable={false} visible={isOutdated}>
            <Dialog.Title>{t("login.newVersion.title")}</Dialog.Title>
            <Dialog.Content>
              <Paragraph>{t("login.newVersion.content")}</Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button onPress={handleUpdateButtonClick}>{t("login.newVersion.btn")}</Button>
            </Dialog.Actions>
          </Dialog>
        </Portal>
      </View>
    </React.StrictMode>
  );
};

export { loginView as LoginView };
