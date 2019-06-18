import { default as ApolloClient, Operation } from "apollo-boost";
import { default as Constants } from "expo-constants";
import * as SecureStore from "expo-secure-store";
import _ from "lodash";
import unfetch from "unfetch";

const apiHost: string = Constants.appOwnership === "expo"
  ? `http://${String(Constants.manifest.hostUri)
    .split(":")[0]}`
  : "https://fluidattacks.com";

export const client: ApolloClient<{}> = new ApolloClient<{}>({
  fetch: _.isUndefined(fetch) ? unfetch : fetch,
  request: async (operation: Operation): Promise<void> => {
    const token: string =
      await SecureStore.getItemAsync("integrates_session") as string;

    operation.setContext({
      headers: {
        authorization: `Bearer ${token}`,
      },
    });
  },
  uri: `${apiHost}/integrates/api`,
});
