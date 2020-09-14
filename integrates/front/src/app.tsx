import { BugsnagErrorBoundary } from "utils/bugsnagErrorBoundary";
import { Dashboard } from "scenes/Dashboard";
import { Login } from "scenes/Login";
import { NetworkStatus } from "react-apollo-network-status";
import { Preloader } from "components/Preloader";
import React from "react";
import ReactDOM from "react-dom";
import { Provider as ReduxProvider } from "react-redux";
import { Registration } from "scenes/Registration";
import { ToastContainer } from "react-toastify";
import mixpanel from "mixpanel-browser";
import store from "store";
import { ApolloProvider, networkStatusNotifier } from "utils/apollo";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "utils/authz/config";
import { secureStore, secureStoreContext } from "utils/secureStore";
import "react-toastify/dist/ReactToastify.min.css";

const App: React.FC = (): JSX.Element => {
  const status: NetworkStatus = networkStatusNotifier.useApolloNetworkStatus();
  const isLoading: boolean =
    status.numPendingQueries > 0 || status.numPendingMutations > 0;

  return (
    <React.StrictMode>
      <BugsnagErrorBoundary>
        <BrowserRouter basename={"/"}>
          <ApolloProvider>
            <ReduxProvider store={store}>
              <authzPermissionsContext.Provider value={userLevelPermissions}>
                <secureStoreContext.Provider value={secureStore}>
                  <Switch>
                    <Route component={Login} exact={true} path={"/"} />
                    <Route component={Registration} path={"/registration"} />
                    <Route component={Dashboard} path={"/"} />
                  </Switch>
                </secureStoreContext.Provider>
                {isLoading ? <Preloader /> : undefined}
              </authzPermissionsContext.Provider>
            </ReduxProvider>
          </ApolloProvider>
        </BrowserRouter>
        <ToastContainer
          autoClose={5000}
          closeOnClick={false}
          hideProgressBar={true}
          position={"top-right"}
        />
      </BugsnagErrorBoundary>
    </React.StrictMode>
  );
};

const extendedModule: NodeModule & {
  hot?: { accept: () => void };
} = module as NodeModule & {
  hot?: { accept: () => void };
};
if (extendedModule.hot !== undefined) {
  extendedModule.hot.accept();
}

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
ReactDOM.render(React.createElement(App), document.getElementById("root"));
