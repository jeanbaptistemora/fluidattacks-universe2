import { registerRootComponent } from "expo";
import { isRootedExperimentalAsync } from "expo-device";
import {
  SecurityLevel,
  getEnrolledLevelAsync,
} from "expo-local-authentication";
import { getItemAsync } from "expo-secure-store";
import _ from "lodash";
import React, { useCallback, useEffect, useMemo, useState } from "react";
import { I18nextProvider, useTranslation } from "react-i18next";
import { Alert, StatusBar, View, useColorScheme } from "react-native";
import type { ColorSchemeName } from "react-native";
import {
  DarkTheme,
  DefaultTheme,
  Provider as PaperProvider,
} from "react-native-paper";
import {
  BackButton,
  NativeRouter,
  Redirect,
  Route,
  Switch,
} from "react-router-native";

import { DashboardView } from "./containers/DashboardView";
import { LockView } from "./containers/LockView";
import { LoginView } from "./containers/LoginView";
import { WelcomeView } from "./containers/WelcomeView";
import { ApolloProvider } from "./utils/apollo";
import { BugsnagErrorBoundary } from "./utils/bugsnagErrorBoundary";
import type { ISessionTokenContext } from "./utils/sessionToken/context";
import { SessionToken } from "./utils/sessionToken/context";
import { i18next } from "./utils/translations/translate";

const lightTheme: ReactNativePaper.Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    accent: "#FF3435",
    background: "#FFFFFF",
    primary: "#FF3435",
  },
};

const darkTheme: ReactNativePaper.Theme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    accent: "#FF3435",
    primary: "#FF3435",
  },
};

const App: React.FunctionComponent = (): JSX.Element => {
  const colorScheme: ColorSchemeName = useColorScheme();
  const { t } = useTranslation();

  // State management
  const [isLoggedIn, setLoggedIn] = useState<boolean | undefined>(undefined);
  const [sessionToken, setSessionToken] = useState<string>("");
  const sessionTokenValue = useMemo(
    (): ISessionTokenContext => [sessionToken, setSessionToken],
    [sessionToken, setSessionToken]
  );

  // Side effects
  const checkAuth: () => void = useCallback(async (): Promise<void> => {
    try {
      // eslint-disable-next-line fp/no-let
      let token: string | null = _.isEmpty(sessionToken) ? null : sessionToken;
      const authState: string | null = await getItemAsync("authState");

      if (_.isNil(token)) {
        await getEnrolledLevelAsync().then(
          async (value: SecurityLevel): Promise<void> => {
            if (value === SecurityLevel.BIOMETRIC) {
              // eslint-disable-next-line fp/no-mutation
              token = await getItemAsync("session_token");
              if (!_.isNil(token)) {
                setSessionToken(token);
              }
            }
          }
        );
      }

      setLoggedIn(!(_.isNil(token) || _.isNil(authState)));
    } catch {
      setLoggedIn(false);
    }
  }, [sessionToken]);

  useEffect((): void => {
    const onMount = async (): Promise<void> => {
      if (await isRootedExperimentalAsync()) {
        Alert.alert(t("root.title"), t("root.msg"), [], { cancelable: false });
      } else {
        checkAuth();
      }
    };
    void onMount();
  }, [checkAuth, t]);

  const theme: ReactNativePaper.Theme =
    colorScheme === "dark" ? darkTheme : lightTheme;
  const rootView: JSX.Element =
    isLoggedIn === undefined ? (
      // eslint-disable-next-line react/forbid-component-props
      <View style={{ backgroundColor: theme.colors.background, flex: 1 }} />
    ) : isLoggedIn ? (
      <Redirect to={"/Lock"} />
    ) : (
      <Redirect to={"/Login"} />
    );

  return (
    <React.StrictMode>
      <BugsnagErrorBoundary>
        <NativeRouter>
          <PaperProvider theme={theme}>
            <I18nextProvider i18n={i18next}>
              <StatusBar
                backgroundColor={"transparent"}
                barStyle={
                  colorScheme === "dark" ? "light-content" : "dark-content"
                }
                translucent={true}
              />
              <SessionToken.Provider value={sessionTokenValue}>
                <ApolloProvider>
                  <BackButton>
                    <Switch>
                      <Route exact={true} path={"/"}>
                        {rootView}
                      </Route>
                      <Route component={LockView} exact={true} path={"/Lock"} />
                      <Route
                        component={LoginView}
                        exact={true}
                        path={"/Login"}
                      />
                      <Route
                        component={WelcomeView}
                        exact={true}
                        path={"/Welcome"}
                      />
                      <Route
                        component={DashboardView}
                        exact={true}
                        path={"/Dashboard"}
                      />
                    </Switch>
                  </BackButton>
                </ApolloProvider>
              </SessionToken.Provider>
            </I18nextProvider>
          </PaperProvider>
        </NativeRouter>
      </BugsnagErrorBoundary>
    </React.StrictMode>
  );
};

registerRootComponent(App);

export { App };
