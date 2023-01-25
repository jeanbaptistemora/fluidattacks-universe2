import React from "react";
import { render } from "react-dom";

import { App } from "./App";

// eslint-disable-next-line @typescript-eslint/no-unused-vars
declare const acquireVsCodeApi: <T = unknown>() => {
  getState: () => T;
  setState: (data: T) => void;
  postMessage: (msg: unknown) => void;
};

const elm = document.querySelector("#root");
if (elm) {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  render(<App />, elm);
}

// Webpack HMR
// eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any, @typescript-eslint/strict-boolean-expressions
if ((module as any).hot) {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any, @typescript-eslint/strict-boolean-expressions, @typescript-eslint/no-unsafe-call
  (module as any).hot.accept();
}
