import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
} from "@apollo/client/core";
import type { NormalizedCacheObject } from "@apollo/client/core";
import { setContext } from "@apollo/client/link/context";
import fetch from "cross-fetch";
// eslint-disable-next-line import/no-unresolved
import { window, workspace } from "vscode";

const getClient = (): ApolloClient<NormalizedCacheObject> => {
  const authLink = setContext(
    (): {
      headers: {
        Authorization: string;
      };
    } => {
      const token: string =
        (workspace.getConfiguration("retrieves").get("api_token") ?? "") ||
        (process.env.INTEGRATES_API_TOKEN ?? "");
      if (token.length === 0) {
        void window.showWarningMessage("Can not find the integrates api token");
      }

      return {
        headers: {
          // eslint-disable-next-line @typescript-eslint/naming-convention
          Authorization: `Bearer ${token}`,
        },
      };
    }
  );
  const httpLink = createHttpLink({
    fetch,
    uri: "https://app.fluidattacks.com/api",
  });

  return new ApolloClient({
    cache: new InMemoryCache({}),
    link: authLink.concat(httpLink),
  });
};

const API_CLIENT = getClient();

export { API_CLIENT };
