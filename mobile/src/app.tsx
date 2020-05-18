import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";
import { I18nextProvider } from "react-i18next";
import { StatusBar } from "react-native";
import { DefaultTheme, Provider as PaperProvider, Theme } from "react-native-paper";
import { BackButton, NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";
import { WelcomeView } from "./containers/WelcomeView";
import { client } from "./utils/apollo";
import { i18next } from "./utils/translations/translate";

const theme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    accent: "#FF3435",
    primary: "#FF3435",
  },
  dark: false,
};

/* tslint:disable-next-line: variable-name
 * The root component name must be 'App' for fast refresh to work properly
 * export/import aliases won't work
 */
export const App: React.FunctionComponent = (): JSX.Element => (
  <ApolloProvider client={client}>
    <PaperProvider theme={theme}>
      <I18nextProvider i18n={i18next}>
        <StatusBar backgroundColor="transparent" barStyle="light-content" translucent={true} />
        <NativeRouter>
          <BackButton>
            <Switch>
              <Route path="/" component={LoginView} exact={true} />
              <Route path="/Welcome" component={WelcomeView} exact={true} />
              <Route path="/Menu" component={MenuView} exact={true} />
            </Switch>
          </BackButton>
        </NativeRouter>
      </I18nextProvider>
    </PaperProvider>
  </ApolloProvider>
);
