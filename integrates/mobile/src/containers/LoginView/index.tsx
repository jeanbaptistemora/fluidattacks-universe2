import Bugsnag from "@bugsnag/expo";
// Needed for correct usage of NativeConstants.appOwnership
import Constants, { AppOwnership } from "expo-constants"; // eslint-disable-line import/no-named-as-default
import type { NativeConstants } from "expo-constants";
import { setItemAsync } from "expo-secure-store";
import {
  coolDownAsync,
  maybeCompleteAuthSession,
  warmUpAsync,
} from "expo-web-browser";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Linking, View } from "react-native";
import {
  Button,
  Dialog,
  Paragraph,
  Portal,
  useTheme,
} from "react-native-paper";
import { useHistory } from "react-router-native";

import { BitbucketButton } from "./BitbucketButton";
import { GoogleButton } from "./GoogleButton";
import { MicrosoftButton } from "./MicrosoftButton";
import { styles } from "./styles";
import { getOutdatedStatus } from "./version";

import { About } from "../../components/About";
import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import {
  authWithBitbucket,
  authWithGoogle,
  authWithMicrosoft,
} from "../../utils/socialAuth";
import type { IAuthResult } from "../../utils/socialAuth";

// eslint-disable-next-line @typescript-eslint/no-type-alias
type manifestStructure = NativeConstants["manifest"] & {
  android: { package: string };
};
const manifest: manifestStructure = Constants.manifest as manifestStructure;

maybeCompleteAuthSession();

const LoginView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();

  // State management
  const [isLoading, setIsLoading] = useState(true);
  const [isOutdated, setIsOutdated] = useState(false);

  // Side effects
  useEffect((): void => {
    const checkVersion: () => void = async (): Promise<void> => {
      const shouldSkip: boolean = Constants.appOwnership === AppOwnership.Expo;

      if (!shouldSkip) {
        setIsOutdated(await getOutdatedStatus());
      }
      setIsLoading(false);
    };
    checkVersion();
  }, []);

  useEffect((): (() => void) => {
    /*
     * Performance optimization for the login process
     *
     * @see https://docs.expo.io/guides/authentication/#warming-the-browser
     */
    void warmUpAsync();

    return (): void => {
      void coolDownAsync();
    };
  }, []);

  // Event handlers
  const handleBitbucketLogin: () => void = async (): Promise<void> => {
    setIsLoading(true);

    const result: IAuthResult = await authWithBitbucket();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName
      );
      await setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setIsLoading(false);
    }
  };

  const handleGoogleLogin: () => void = async (): Promise<void> => {
    setIsLoading(true);

    const result: IAuthResult = await authWithGoogle();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName
      );
      await setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setIsLoading(false);
    }
  };

  const handleMicrosoftLogin: () => void = async (): Promise<void> => {
    setIsLoading(true);

    const result: IAuthResult = await authWithMicrosoft();
    if (result.type === "success") {
      Bugsnag.setUser(
        result.user.email,
        result.user.email,
        result.user.firstName
      );
      await setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setIsLoading(false);
    }
  };

  const handleUpdateButtonClick: () => void = async (): Promise<void> => {
    await Linking.openURL(`market://details?id=${manifest.android.package}`);
  };

  return (
    <React.StrictMode>
      {/* Needed to override styles */}
      {/* eslint-disable-next-line react/forbid-component-props*/}
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Logo fill={colors.text} height={180} width={300} />
        {/* eslint-disable-next-line react/forbid-component-props*/}
        <View style={styles.buttonsContainer}>
          <GoogleButton
            disabled={isLoading ? true : isOutdated}
            //  Unexpected behaviour with no-bind
            onPress={handleGoogleLogin} // eslint-disable-line react/jsx-no-bind
          />
          <MicrosoftButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleMicrosoftLogin} // eslint-disable-line react/jsx-no-bind
          />
          <BitbucketButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleBitbucketLogin} // eslint-disable-line react/jsx-no-bind
          />
        </View>
        <Preloader visible={isLoading} />
        {/* eslint-disable-next-line react/forbid-component-props*/}
        <View style={styles.bottom}>
          <About />
        </View>
        <Portal>
          <Dialog dismissable={false} visible={isOutdated}>
            <Dialog.Title>{t("login.newVersion.title")}</Dialog.Title>
            <Dialog.Content>
              <Paragraph>{t("login.newVersion.content")}</Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button
                onPress={handleUpdateButtonClick} // eslint-disable-line react/jsx-no-bind
              >
                {t("login.newVersion.btn")}
              </Button>
            </Dialog.Actions>
          </Dialog>
        </Portal>
      </View>
    </React.StrictMode>
  );
};

export { LoginView };
