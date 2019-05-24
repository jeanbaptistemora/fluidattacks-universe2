import { Constants } from "expo";
import React from "react";
import { ApolloProvider } from "react-apollo";
import { Provider } from "react-redux";
import { NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";
import { WelcomeView } from "./containers/WelcomeView";
import { store } from "./store";
import { client } from "./utils/apollo";

const app: React.FunctionComponent = (): JSX.Element => (
  <ApolloProvider client={client}>
    <Provider store={store}>
      <NativeRouter>
        <Switch>
          <Route path="/" component={LoginView} exact={true} />
          <Route path="/Welcome" component={WelcomeView} />
          <Route path="/Menu" component={MenuView} />
        </Switch>
      </NativeRouter>
    </Provider>
  </ApolloProvider>
);

export { app as App };
