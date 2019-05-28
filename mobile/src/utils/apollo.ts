import { default as ApolloClient, Operation } from "apollo-boost";
import { Constants, SecureStore } from "expo";

const apiHost: string = Constants.appOwnership === "expo"
  ? `http://${String(Constants.manifest.hostUri)
    .split(":")[0]}`
  : "https://fluidattacks.com";

export const client: ApolloClient<{}> = new ApolloClient<{}>({
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
