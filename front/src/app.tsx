import mixpanel from "mixpanel-browser";
import React from "react";
import { ApolloProvider } from "react-apollo";
import ReactDOM from "react-dom";
import { Provider } from "react-redux";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import { ToastContainer } from "react-toastify";
/* tslint:disable-next-line:no-import-side-effect no-submodule-imports
 * Disabling this two rules is necessary for
 * allowing the import of default styles that ReactToastify needs
 * to display properly even if some of them are overridden later
 */
import "react-toastify/dist/ReactToastify.min.css";
import { Preloader } from "./components/Preloader";
import Dashboard from "./scenes/Dashboard";
import { default as Registration } from "./scenes/Registration";
import store from "./store/index";
import { client } from "./utils/apollo";

const app: React.FC = (): JSX.Element => (
  <React.StrictMode>
    <BrowserRouter basename="/integrates">
      <React.Fragment>
        <ApolloProvider client={client}>
          <Provider store={store}>
            <React.Fragment>
              <Switch>
                <Route path="/registration" component={Registration} />
                <Route path="/dashboard" component={Dashboard} />
              </Switch>
            <Preloader />
            </React.Fragment>
          </Provider>
        </ApolloProvider>
      </React.Fragment>
    </BrowserRouter>
    <ToastContainer position="top-right" autoClose={5000} hideProgressBar={true} closeOnClick={false} />
  </React.StrictMode>
);

mixpanel.init("7a7ceb75ff1eed29f976310933d1cc3e");
ReactDOM.render(React.createElement(app), document.getElementById("root"));
