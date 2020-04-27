import { ApolloProvider } from "@apollo/react-hooks";
import React from "react";
import { StatusBar } from "react-native";
import { DefaultTheme, Provider as ThemeProvider, ThemeShape } from "react-native-paper";
import { Provider as ReduxProvider } from "react-redux";
import { NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";
import { WelcomeView } from "./containers/WelcomeView";
import { store } from "./store";
import { client } from "./utils/apollo";

const theme: ThemeShape = {
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
    <ReduxProvider store={store}>
      <ThemeProvider theme={theme}>
        <StatusBar barStyle="light-content" />
        <NativeRouter>
          <Switch>
            <Route path="/" component={LoginView} exact={true} />
            <Route path="/Welcome" component={WelcomeView} />
            <Route path="/Menu" component={MenuView} />
          </Switch>
        </NativeRouter>
      </ThemeProvider>
    </ReduxProvider>
  </ApolloProvider>
);

export { app as App };
