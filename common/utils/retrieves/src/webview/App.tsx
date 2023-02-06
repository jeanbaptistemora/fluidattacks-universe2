import { ApolloProvider } from "@apollo/client";
import { messageHandler } from "@estruyf/vscode/dist/client";
import React, { useMemo, useState } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import { GitEnvironmentUrls } from "./containers/GitEnvironmentUrls";
import { ToeLines } from "./containers/ToeLines";

import { getClient } from "../utils/api";

import "./styles.css";

const App = (): JSX.Element => {
  const [apiToken, setApiToken] = useState<string>("");
  const [route, setRoute] = useState<string>();

  useMemo((): void => {
    void messageHandler.request<string>("GET_ROUTE").then((msg): void => {
      setRoute(msg);
    });
  }, []);

  useMemo((): void => {
    void messageHandler.request<string>("GET_API_TOKEN").then((msg): void => {
      setApiToken(msg);
    });
  }, []);

  if (route === undefined) {
    return <div />;
  }

  return (
    <ApolloProvider client={getClient(apiToken)}>
      <div className={"app"}>
        <MemoryRouter initialEntries={[`/${route}`]}>
          <Routes>
            <Route element={<ToeLines />} path={"toeLines"} />
            <Route
              element={<GitEnvironmentUrls />}
              path={"gitEnvironmentUrls"}
            />
          </Routes>
        </MemoryRouter>
      </div>
    </ApolloProvider>
  );
};

export { App };
