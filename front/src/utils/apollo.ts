import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink } from "apollo-link";
import { ErrorResponse, onError } from "apollo-link-error";
import { createUploadLink } from "apollo-upload-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import { getEnvironment } from "./context";

const getCookie: (name: string) => string = (name: string): string => {
  let cookieValue: string;
  cookieValue = "";
  if (document.cookie !== "") {
    let cookie: string;
    const cookies: string[] = document.cookie.split(";");
    for (cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === `${name}=`) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
};

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  connectToDevTools: getEnvironment() !== "production",
  defaultOptions: {
    query: {
      fetchPolicy: "cache-and-network",
    },
    watchQuery: {
      fetchPolicy: "cache-and-network",
    },
  },
  link: ApolloLink.from([
    onError(({ graphQLErrors, networkError }: ErrorResponse): void => {
      if (networkError !== undefined) {
        const { statusCode } = (networkError as { statusCode: number });

        if (statusCode === 403) {
          // Django CSRF expired
          location.reload();
        }
      } else if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(({ message }: GraphQLError) => {
          if (_.includes(["Login required", "Exception - Invalid Authorization"], message)) {
            location.assign("/integrates/logout");
          }
        });
      }
    }),
    createUploadLink({
      credentials: "same-origin",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      uri: `${window.location.origin}/integrates/api`,
    }),
  ]),
});
