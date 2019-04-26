// @ts-check

import { KeepAwake, registerRootComponent } from "expo";
import { app } from "./src/App";

if (__DEV__) {
  KeepAwake.activate();
}

registerRootComponent(app);
