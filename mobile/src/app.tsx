import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { ColorSchemeName, StatusBar, useColorScheme, View } from "react-native";
import { DarkTheme, DefaultTheme, Provider as PaperProvider, Theme } from "react-native-paper";
import { BackButton, NativeRouter, Redirect, Route, Switch } from "react-router-native";

import { DashboardView } from "./containers/DashboardView";
import { LockView } from "./containers/LockView";
import { LoginView } from "./containers/LoginView";
import { WelcomeView } from "./containers/WelcomeView";
import { ApolloProvider } from "./utils/apollo";
import { i18next } from "./utils/translations/translate";

const lightTheme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    accent: "#FF3435",
    background: "#FFFFFF",
    primary: "#FF3435",
  },
};

const darkTheme: Theme = {
  ...DarkTheme,
  colors: {
    ...DarkTheme.colors,
    accent: "#FF3435",
    primary: "#FF3435",
  },
};

/* tslint:disable-next-line: variable-name
* The root component name must be 'App' for fast refresh to work properly
* export/import aliases won't work
*/
export const App: React.FunctionComponent = (): JSX.Element => {
  const colorScheme: ColorSchemeName = useColorScheme();

  // State management
  const [
    isLoggedIn,
    setLoggedIn,
  ] = React.useState<boolean | undefined>(undefined);

  // Side effects
  const checkAuth: (() => void) = async (): Promise<void> => {
    const token: string | null =
      await SecureStore.getItemAsync("integrates_session");
    const authState: string | null =
      await SecureStore.getItemAsync("authState");

    setLoggedIn(_.isNil(token) || _.isNil(authState) ? false : true);
  };

  const onMount: (() => void) = (): void => {
    checkAuth();
  };

  React.useEffect(onMount, []);

  const theme: Theme = colorScheme === "dark" ? darkTheme : lightTheme;
  const rootView: JSX.Element = isLoggedIn === undefined
    ? <View style={{ backgroundColor: theme.colors.background, flex: 1 }} />
    : isLoggedIn
      ? <LockView />
      : <Redirect to="/Login" />;

  return (
    <React.StrictMode>
      <NativeRouter>
        <PaperProvider theme={theme}>
          <I18nextProvider i18n={i18next}>
            <StatusBar
              backgroundColor="transparent"
              barStyle={colorScheme === "dark"
                ? "light-content"
                : "dark-content"}
              translucent={true}
            />
            <ApolloProvider>
              <BackButton>
                <Switch>
                  <Route path="/" exact={true}>{rootView}</Route>
                  <Route path="/Login" component={LoginView} exact={true} />
                  <Route path="/Welcome" component={WelcomeView} exact={true} />
                  <Route
                    path="/Dashboard"
                    component={DashboardView}
                    exact={true}
                  />
                </Switch>
              </BackButton>
            </ApolloProvider>
          </I18nextProvider>
        </PaperProvider>
      </NativeRouter>
    </React.StrictMode>
  );
};
