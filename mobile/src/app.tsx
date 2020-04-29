import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";
import { StatusBar } from "react-native";
import { DefaultTheme, Provider as ThemeProvider, Theme } from "react-native-paper";
import { NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";
import { WelcomeView } from "./containers/WelcomeView";
import { client } from "./utils/apollo";

export const theme: Theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    accent: "#272727",
    primary: "#ff3435",
  },
  dark: true,
};

const app: React.FunctionComponent = (): JSX.Element => (
  <ApolloProvider client={client}>
    <ThemeProvider theme={theme}>
      <StatusBar barStyle="light-content" />
      <NativeRouter>
        <Switch>
          <Route path="/" component={LoginView} exact={true} />
          <Route path="/Welcome" component={WelcomeView} exact={true} />
          <Route path="/Menu" component={MenuView} exact={true} />
        </Switch>
      </NativeRouter>
    </ThemeProvider>
  </ApolloProvider>
);

export { app as App };
