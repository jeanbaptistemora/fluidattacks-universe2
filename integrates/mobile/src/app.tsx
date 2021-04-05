import { registerRootComponent } from "expo";
import { getItemAsync } from "expo-secure-store";
import _ from "lodash";
import React, { useEffect, useState } from "react";
import { I18nextProvider } from "react-i18next";
import type { ColorSchemeName } from "react-native";
import { StatusBar, View, useColorScheme } from "react-native";
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

  // State management
  const [isLoggedIn, setLoggedIn] = useState<boolean | undefined>(undefined);

  // Side effects
  const checkAuth: () => void = async (): Promise<void> => {
    try {
      const token: string | null = await getItemAsync("integrates_session");
      const authState: string | null = await getItemAsync("authState");
      setLoggedIn(!(_.isNil(token) || _.isNil(authState)));
    } catch {
      setLoggedIn(false);
    }
  };

  const onMount: () => void = (): void => {
    checkAuth();
  };

  useEffect(onMount, []);

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
              <ApolloProvider>
                <BackButton>
                  <Switch>
                    <Route exact={true} path={"/"}>
                      {rootView}
                    </Route>
                    <Route component={LockView} exact={true} path={"/Lock"} />
                    <Route component={LoginView} exact={true} path={"/Login"} />
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
            </I18nextProvider>
          </PaperProvider>
        </NativeRouter>
      </BugsnagErrorBoundary>
    </React.StrictMode>
  );
};

registerRootComponent(App);

export { App };
