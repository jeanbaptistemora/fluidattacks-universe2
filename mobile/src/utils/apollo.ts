import { default as ApolloClient } from "apollo-boost";
import { Constants } from "expo";

const apiHost: string = Constants.appOwnership === "expo"
  ? `http://${String(Constants.manifest.hostUri)
    .split(":")[0]}`
  : "https://fluidattacks.com";

export const client: ApolloClient<{}> = new ApolloClient<{}>({
  uri: `${apiHost}/integrates/api`,
});
