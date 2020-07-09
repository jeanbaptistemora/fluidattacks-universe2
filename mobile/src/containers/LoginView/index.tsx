import {
  AppOwnership, default as Constants, NativeConstants,
} from "expo-constants";
import * as SecureStore from "expo-secure-store";
import * as Updates from "expo-updates";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { Linking, Platform, View } from "react-native";
import {
  Button, Dialog, Paragraph, Portal, Text, useTheme,
} from "react-native-paper";
import { useHistory } from "react-router-native";

import { Logo } from "../../components/Logo";
import { Preloader } from "../../components/Preloader";
import { rollbar } from "../../utils/rollbar";
import {
  authWithGoogle, authWithMicrosoft, IAuthResult,
} from "../../utils/socialAuth";

import { GoogleButton } from "./GoogleButton";
import { MicrosoftButton } from "./MicrosoftButton";
import { styles } from "./styles";
import { checkPlayStoreVersion } from "./version";

type manifestStructure = NativeConstants["manifest"] & {
  android: { package: string };
};
const manifest: manifestStructure = (Constants.manifest as manifestStructure);

const loginView: React.FunctionComponent = (): JSX.Element => {
  const history: ReturnType<typeof useHistory> = useHistory();
  const { colors } = useTheme();
  const { t } = useTranslation();

  // State management
  const [isLoading, setLoading] = React.useState(true);
  const [isOutdated, setOutdated] = React.useState(false);

  const checkVersion: (() => void) = async (): Promise<void> => {
    const shouldSkipCheck: boolean =
      Platform.OS === "ios"
      || Constants.appOwnership === AppOwnership.Expo;

    if (!shouldSkipCheck) {
      setOutdated(await checkPlayStoreVersion());
    }
    setLoading(false);
  };

  const onMount: (() => void) = (): void => {
    checkVersion();
  };
  React.useEffect(onMount, []);

  // Event handlers
  const handleGoogleButtonClick: (() => void) = async (): Promise<void> => {
    setLoading(true);

    const result: IAuthResult = await authWithGoogle();
    if (result.type === "success") {
      rollbar.setPerson({ id: result.user.email });
      await SecureStore.setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setLoading(false);
    }
  };

  const handleMicrosoftButtonClick: (() => void) = async (): Promise<void> => {
    setLoading(true);

    const result: IAuthResult = await authWithMicrosoft();
    if (result.type === "success") {
      rollbar.setPerson({ id: result.user.email });
      await SecureStore.setItemAsync("authState", JSON.stringify(result));
      history.replace("/Welcome", result);
    } else {
      setLoading(false);
    }
  };

  const handleUpdateButtonClick: (() => void) = async (): Promise<void> => {
    await Linking.openURL(`market://details?id=${manifest.android.package}`);
  };

  return (
    <React.StrictMode>
      <View style={[styles.container, { backgroundColor: colors.background }]}>
        <Logo width={300} height={70} fill={colors.text} />
        <View style={styles.buttonsContainer}>
          <GoogleButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleGoogleButtonClick}
          />
          <MicrosoftButton
            disabled={isLoading ? true : isOutdated}
            onPress={handleMicrosoftButtonClick}
          />
        </View>
        <Preloader visible={isLoading} />
        <View style={styles.bottom}>
          <Text accessibilityStates="">{t("common.slogan")}</Text>
          <Text accessibilityStates="">
            v. {(Updates.manifest as Updates.Manifest).version}
          </Text>
        </View>
        <Portal>
          <Dialog dismissable={false} visible={isOutdated}>
            <Dialog.Title accessibilityStates="">
              {t("login.newVersion.title")}
            </Dialog.Title>
            <Dialog.Content>
              <Paragraph>{t("login.newVersion.content")}</Paragraph>
            </Dialog.Content>
            <Dialog.Actions>
              <Button accessibilityStates="" onPress={handleUpdateButtonClick}>
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
