import Bugsnag from "@bugsnag/expo";
import {
  AppOwnership,
  default as Constants,
  NativeConstants,
} from "expo-constants";
import * as SecureStore from "expo-secure-store";
import {
  coolDownAsync,
  maybeCompleteAuthSession,
  warmUpAsync,
} from "expo-web-browser";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Linking, Platform, View } from "react-native";
import {
  Button,
  Dialog,
  Paragraph,
  Portal,
  Text,
  useTheme,
} from "react-native-paper";
import { useHistory } from "react-router-native";

import { About } from "../../components/About";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import {
  authWithBitbucket,
  authWithGoogle,
  authWithMicrosoft,
  IAuthResult,
} from "../../utils/socialAuth";

import { BitbucketButton } from "./BitbucketButton";
import { GoogleButton } from "./GoogleButton";
import { MicrosoftButton } from "./MicrosoftButton";
import { styles } from "./styles";
import { checkPlayStoreVersion } from "./version";

type manifestStructure = NativeConstants["manifest"] & {
  android: { package: string };
};
const manifest: manifestStructure = Constants.manifest as manifestStructure;

maybeCompleteAuthSession();

const loginView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();

  // State management
  const [isLoading, setLoading] = React.useState(true);
  const [isOutdated, setOutdated] = React.useState(false);

  // Side effects
  React.useEffect((): void => {
    const checkVersion: () => void = async (): Promise<void> => {
      const shouldSkipCheck: boolean =
        Platform.OS === "ios" || Constants.appOwnership === AppOwnership.Expo;

      if (!shouldSkipCheck) {
        setOutdated(await checkPlayStoreVersion());
      }
      setLoading(false);
    };
    checkVersion();
  },              []);

  React.useEffect((): (() => void) => {
    /* Performance optimization for the login process
     *
     * @see https://docs.expo.io/guides/authentication/#warming-the-browser
     */
    void warmUpAsync();

    return (): void => {
      void coolDownAsync();
    };
  },              []);

  // Event handlers
  const handleBitbucketLogin: () => void = async (): Promise<void> => {
    setLoading(true);

    const result: IAuthResult = await authWithBitbucket();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName,
      );
      await SecureStore.setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setLoading(false);
    }
  };

  const handleGoogleLogin: () => void = async (): Promise<void> => {
    setLoading(true);

    const result: IAuthResult = await authWithGoogle();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName,
      );
      await SecureStore.setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setLoading(false);
    }
  };

  const handleMicrosoftLogin: () => void = async (): Promise<void> => {
    setLoading(true);

    const result: IAuthResult = await authWithMicrosoft();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName,
      );
      await SecureStore.setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setLoading(false);
    }
  };

  const handleUpdateButtonClick: () => void = async (): Promise<void> => {
    await Linking.openURL(`market://details?id=${manifest.android.package}`);
  };

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Logo width={300} height={70} fill={colors.text} />
        <View style={styles.buttonsContainer}>
          <GoogleButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleGoogleLogin}
          />
          <MicrosoftButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleMicrosoftLogin}
          />
          <BitbucketButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleBitbucketLogin}
          />
        </View>
        <Preloader visible={isLoading} />
        <View style={styles.bottom}>
          <Text>{t("common.slogan")}</Text>
          <About />
        </View>
        <Portal>
          <Dialog dismissable={false} visible={isOutdated}>
            <Dialog.Title>{t("login.newVersion.title")}</Dialog.Title>
            <Dialog.Content>
              <Paragraph>{t("login.newVersion.content")}</Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button onPress={handleUpdateButtonClick}>
                {t("login.newVersion.btn")}
              </Button>
            </Dialog.Actions>
          </Dialog>
        </Portal>
      </View>
    </React.StrictMode>
  );
};

export { loginView as LoginView };
