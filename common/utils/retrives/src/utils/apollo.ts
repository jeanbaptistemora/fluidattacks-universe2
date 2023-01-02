import { ApolloClient, createHttpLink, InMemoryCache } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import * as vscode from "vscode";

const httpLink = createHttpLink({
  uri: "https://app.fluidattacks.com/api",
  fetch,
});

const authLink = setContext(() => {
  const token: undefined | string = vscode.workspace
    .getConfiguration("retrieves")
    .get("api_token");
  return {
    headers: {
      // eslint-disable-next-line @typescript-eslint/naming-convention
      Authorization: token,
    },
  };
});

const getClient = () =>
  new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache(),
  });
