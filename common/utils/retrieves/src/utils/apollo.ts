import {
  ApolloClient,
  InMemoryCache,
  createHttpLink,
} from "@apollo/client/core";
import type { NormalizedCacheObject } from "@apollo/client/core";
import { setContext } from "@apollo/client/link/context";
import fetch from "cross-fetch";
// eslint-disable-next-line import/no-unresolved
import { workspace } from "vscode";

const getClient = (): ApolloClient<NormalizedCacheObject> => {
  const authLink = setContext(
    (): {
      headers: {
        Authorization: string;
      };
    } => {
      const token: string | undefined =
        (process.env.INTEGRATES_API_TOKEN ?? "") ||
        workspace.getConfiguration("retrieves").get("api_token");

      return {
        headers: {
          // eslint-disable-next-line @typescript-eslint/naming-convention
          Authorization: `Bearer ${token ?? ""}`,
        },
      };
    }
  );
  const httpLink = createHttpLink({
    fetch,
    uri: "https://app.fluidattacks.com/api",
  });

  return new ApolloClient({
    cache: new InMemoryCache(),
    link: authLink.concat(httpLink),
  });
};

export { getClient };
