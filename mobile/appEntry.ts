import { registerRootComponent } from "expo";
import React from "react";
import { AppearanceProvider } from "react-native-appearance";

import { App } from "./src/app";

registerRootComponent((): JSX.Element =>
  React.createElement(AppearanceProvider, undefined, React.createElement(App)));
