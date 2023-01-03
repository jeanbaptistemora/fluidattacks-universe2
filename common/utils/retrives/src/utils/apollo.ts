import {
  ApolloClient,
  createHttpLink,
  InMemoryCache,
} from "@apollo/client/core";
import * as vscode from "vscode";
import { setContext } from "@apollo/client/link/context";

import fetch from "cross-fetch";

const getClient = () => {
  const authLink = setContext(() => {
    const token: undefined | string =
      process.env.INTEGRATES_API_TOKEN ||
      vscode.workspace.getConfiguration("retrieves").get("api_token");
    return {
      headers: {
        // eslint-disable-next-line @typescript-eslint/naming-convention
        Authorization: `Bearer ${token}`,
      },
    };
  });
  const httpLink = createHttpLink({
    uri: "https://app.fluidattacks.com/api",
    fetch,
  });
  return new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache(),
  });
};

export { getClient };
