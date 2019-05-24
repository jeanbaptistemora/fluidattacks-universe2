import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { HttpLink } from "apollo-link-http";
import { Constants } from "expo";

const apiHost: string = Constants.appOwnership === "expo"
  ? `http://${String(Constants.manifest.hostUri)
    .split(":")[0]}`
  : "https://fluidattacks.com";

const httpLink: HttpLink = new HttpLink({
  uri: `${apiHost}/integrates/api`,
});

const cache: InMemoryCache = new InMemoryCache({ resultCaching: true });

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache,
  connectToDevTools: __DEV__,
  link: httpLink,
});
