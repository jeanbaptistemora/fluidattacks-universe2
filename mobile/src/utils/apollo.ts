import { default as ApolloClient, Operation } from "apollo-boost";
import { ErrorResponse } from "apollo-link-error";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import unfetch from "unfetch";

import { getEnvironment } from "./context";
import { rollbar } from "./rollbar";

const apiHost: string = getEnvironment().url;

export const client: ApolloClient<{}> = new ApolloClient<{}>({
  fetch: _.isUndefined(fetch) ? unfetch : fetch,
  onError: (error: ErrorResponse): void => {
    rollbar.error("Error: An error occurred executing API request", error);
  },
  request: async (operation: Operation): Promise<void> => {
    let token: string;
    try {
      token = await SecureStore.getItemAsync("integrates_session") as string;
    } catch (exception) {
      token = "";
      await SecureStore.deleteItemAsync("integrates_session");
    }

    operation.setContext({
      headers: {
        authorization: `Bearer ${token}`,
      },
    });
  },
  uri: `${apiHost}/integrates/api`,
});
