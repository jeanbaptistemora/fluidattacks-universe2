import { createStore, Store } from "redux";
import { getEnvironment } from "../utils/context";
import rootReducer from "./rootReducer";

/* tslint:disable:no-any
 *
 * NO-ANY: Disabling this rule is necessary because TypeScript doesn't
 * recognize custom properties attached to the global window object,
 * which is required to bind redux dev tools browser extension
 */
declare var window: any;
const reduxDevTools: any = (): any =>
  (
    window.__REDUX_DEVTOOLS_EXTENSION__
    ? window.__REDUX_DEVTOOLS_EXTENSION__()
    : undefined
  );
/* tslint:enable:no-any */

const store: Store = createStore(
  rootReducer,
  getEnvironment() === "production"
  ? undefined
  : reduxDevTools(),
);

export = store;
