import { ApolloProvider } from "@apollo/react-hooks";
import mixpanel from "mixpanel-browser";
import React from "react";
import { NetworkStatus } from "react-apollo-network-status";
import ReactDOM from "react-dom";
import { Provider as ReduxProvider } from "react-redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.min.css";
import { Preloader } from "./components/Preloader";
import { Dashboard } from "./scenes/Dashboard";
import { default as Registration } from "./scenes/Registration";
import store from "./store/index";
import { client, networkStatusNotifier } from "./utils/apollo";
import {
  authzPermissionsContext,
  userLevelPermissions,
} from "./utils/authz/config";

const App: React.FC = (): JSX.Element => {
  const status: NetworkStatus = networkStatusNotifier.useApolloNetworkStatus();
  const isLoading: boolean =
    status.numPendingQueries > 0 || status.numPendingMutations > 0;

  return (
    <React.StrictMode>
      <BrowserRouter basename={"/integrates"}>
        <ApolloProvider client={client}>
          <ReduxProvider store={store}>
            <authzPermissionsContext.Provider value={userLevelPermissions}>
              <Switch>
                <Route component={Registration} path={"/registration"} />
                <Route component={Dashboard} path={"/"} />
              </Switch>
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
