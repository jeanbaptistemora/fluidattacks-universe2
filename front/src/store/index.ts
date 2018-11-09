import { applyMiddleware, createStore, Store } from "redux";
import thunk from "redux-thunk";
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
    /* tslint:disable-next-line:strict-type-predicates
     * Disabling this rule is necessary because the following expression is
     * misbelived to be always true by the linter while it is necessary for
     * avoiding errors in the npm test environment where the object window
     * doesn't exist.
     */
    typeof window === "undefined"
    ? undefined
    : window.__REDUX_DEVTOOLS_EXTENSION__
      ? window.__REDUX_DEVTOOLS_EXTENSION__()
      : undefined
  );
/* tslint:enable:no-any */

const store: Store = createStore(
  rootReducer,
  getEnvironment() === "production"
  ? undefined
  : reduxDevTools(),
  applyMiddleware(thunk),
);

export = store;
