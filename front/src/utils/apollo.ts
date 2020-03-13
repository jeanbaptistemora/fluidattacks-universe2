import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import { ApolloLink, Operation } from "apollo-link";
import { ErrorResponse, onError } from "apollo-link-error";
import { createUploadLink } from "apollo-upload-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import { getEnvironment } from "./context";
import { msgError } from "./notifications";
import translate from "./translations/translate";

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

const apiLinkV1: ApolloLink = createUploadLink({
  credentials: "same-origin",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  uri: `${window.location.origin}/integrates/api`,
});

const apiLinkV2: ApolloLink = createUploadLink({
  credentials: "same-origin",
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
  },
  uri: `${window.location.origin}/integrates/v2/api`,
});

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  connectToDevTools: getEnvironment() !== "production",
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "cache-and-network",
    },
  },
  link: ApolloLink.from([
    onError(({ graphQLErrors, networkError, response }: ErrorResponse): void => {
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
          } else if (_.includes(
            ["Access denied", "Exception - Project does not exist", "Exception - Finding not found"],
            message)
          ) {
            if (response !== undefined) {
              response.data = undefined;
              response.errors = undefined;
            }
            msgError(translate.t("proj_alerts.access_denied"));
          }
        });
      }
    }),
    ApolloLink.split(
        // NOTE: Split GraphQL according to migration status
        (operation: Operation) =>
          ["HomeProjects",
           "GetUserAuthorization"].includes(operation.operationName),
        apiLinkV2,
        apiLinkV1,
       ),
  ]),
});
