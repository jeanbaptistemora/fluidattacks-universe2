// tslint:disable: file-name-casing

import React from "react";
import { NativeRouter, Route, Switch } from "react-router-native";

import { LoginView } from "./containers/LoginView";
import { MenuView } from "./containers/MenuView";

const app: React.FunctionComponent = (): JSX.Element => (
  <NativeRouter>
    <Switch>
      <Route path="/" component={LoginView} exact={true} />
      <Route path="/Menu" component={MenuView} />
    </Switch>
  </NativeRouter>
);

export { app as App };
