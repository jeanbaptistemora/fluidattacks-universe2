// tslint:disable: file-name-casing

import React from "react";
import { Provider } from "react-redux";
import { NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";
import { store } from "./store";

const app: React.FunctionComponent = (): JSX.Element => (
  <Provider store={store}>
    <NativeRouter>
      <Switch>
        <Route path="/" component={LoginView} exact={true} />
        <Route path="/Menu" component={MenuView} />
      </Switch>
    </NativeRouter>
  </Provider>
);

export { app as App };
