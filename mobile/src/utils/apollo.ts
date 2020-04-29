import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink } from "apollo-link";
import { setContext } from "apollo-link-context";
import { ErrorResponse, onError } from "apollo-link-error";
import { createHttpLink } from "apollo-link-http";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";

import { getEnvironment } from "./environment";
import { rollbar } from "./rollbar";

const apiHost: string = getEnvironment().url;

const errorLink: ApolloLink = onError((error: ErrorResponse): void => {
  rollbar.error("An error occurred executing API request", error);
});

const authLink: ApolloLink = setContext(async (): Promise<Dictionary> => {
  let token: string;
  try {
    token = await SecureStore.getItemAsync("integrates_session") as string;
  } catch (exception) {
    token = "";
    await SecureStore.deleteItemAsync("integrates_session");
  }

  return {
    headers: {
      authorization: `Bearer ${token}`,
    },
  };
});

const httpLink: ApolloLink = createHttpLink({
  uri: `${apiHost}/integrates/api`,
});

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  link: errorLink.concat(authLink.concat(httpLink)),
});
