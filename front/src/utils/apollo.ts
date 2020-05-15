import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient, ApolloError } from "apollo-client";
import { ApolloLink, Operation } from "apollo-link";
import { ErrorResponse, onError } from "apollo-link-error";
import { WebSocketLink } from "apollo-link-ws";
import { createUploadLink } from "apollo-upload-client";
import { getMainDefinition } from "apollo-utilities";
import { FragmentDefinitionNode, GraphQLError, OperationDefinitionNode } from "graphql";
import _ from "lodash";
import { createNetworkStatusNotifier } from "react-apollo-network-status";
import { getEnvironment } from "./environment";
import { msgError } from "./notifications";
import rollbar from "./rollbar";
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

/**
 * Apollo-compatible wrapper for XHR requests
 *
 * This is a necessary workaround for file upload mutations
 * since the Fetch API that apollo uses by default
 * lacks support for tracking upload progress
 *
 * @see https://github.com/jaydenseric/apollo-upload-client/issues/88
 */
interface IExtendedFetchOptions extends RequestInit {
  notifyUploadProgress: boolean;
  onUploadProgress(ev: ProgressEvent): void;
}

const xhrWrapper: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string, options: IExtendedFetchOptions,
): Promise<Response> => new Promise((
  resolve: (value: Response) => void,
  reject: (reason: Error) => void,
): void => {
  const xhr: XMLHttpRequest = new XMLHttpRequest();

  xhr.onload = (): void => {
    resolve(new Response(xhr.response, options));
  };

  xhr.onerror = (): void => {
    reject(new Error(`Network request failed: ${xhr.responseText}`));
  };

  xhr.ontimeout = (): void => {
    reject(new Error("Network request timed out"));
  };

  xhr.open(_.get(options, "method", "POST"), uri, true);

  if (options.headers !== undefined) {
    Object.keys(options.headers)
      .forEach((key: string): void => {
        xhr.setRequestHeader(key, _.get(options.headers, key));
      });
  }

  xhr.upload.onprogress = options.onUploadProgress;

  xhr.send(options.body);
});

const extendedFetch: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string, options: IExtendedFetchOptions,
): Promise<Response> => {

  const fetchFunction: Promise<Response> = options.notifyUploadProgress
    ? xhrWrapper(uri, options)
    : fetch(uri, options);

  return fetchFunction.then(async (response: Response) => {
    if (response.status !== 200) {

      return Promise.reject(new ApolloError({
        extraInfo: {
          bodyText: await response.text(),
          statusCode: response.status,
        },
        networkError: new Error("NetworkError"),
      }));
    }

    return response;
  });
};

const httpLink: ApolloLink = createUploadLink({
  credentials: "same-origin",
  fetch: extendedFetch,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
    "accept": "application/json",
  },
  uri: `${window.location.origin}/integrates/api`,
});

const wsLink: ApolloLink = new WebSocketLink({
  options: {
    lazy: true,
    reconnect: true,
  },
  uri: `wss://${window.location.host}/integrates/api`,
});

export const networkStatusNotifier: ReturnType<typeof createNetworkStatusNotifier> = createNetworkStatusNotifier();
const apiLink: ApolloLink = ApolloLink.split(
  ({ query }: Operation): boolean => {
    const definition: OperationDefinitionNode | FragmentDefinitionNode = getMainDefinition(query);

    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  networkStatusNotifier.link.concat(httpLink),
);

// Top-level error handling
const errorLink: ApolloLink =
  onError(({ graphQLErrors, networkError, response }: ErrorResponse): void => {
    if (networkError !== undefined) {
      const errorDetails: Dictionary | undefined = _.get(networkError, "extraInfo");

      if (_.isUndefined(errorDetails) || _.isUndefined(errorDetails.statusCode)) {
        msgError(translate.t("proj_alerts.error_network"), "Offline");
      } else {
        const { statusCode } = errorDetails;

        switch (statusCode) {
          case 403:
            // Django CSRF expired
            location.reload();
            break;
          default:
            msgError(translate.t("proj_alerts.error_textsad"));
            rollbar.error("A network error occurred", networkError);
        }
      }
    } else if (graphQLErrors !== undefined) {
      graphQLErrors.forEach(({ message }: GraphQLError) => {
        if (_.includes(["Login required", "Exception - Invalid Authorization"], message)) {
          if (response !== undefined) {
            response.data = {};
            response.errors = [];
          }
          location.assign("/integrates/logout");
        } else if ([
          "Access denied",
          "Exception - Event not found",
          "Exception - Finding not found",
          "Exception - Project does not exist",
        ].includes(message)) {
          if (response !== undefined) {
            response.data = {};
            response.errors = [];
          }
          msgError(translate.t("proj_alerts.access_denied"));
        }
      });
    }
});

export const client: ApolloClient<NormalizedCacheObject> = new ApolloClient({
  cache: new InMemoryCache(),
  connectToDevTools: getEnvironment() !== "production",
  defaultOptions: {
    watchQuery: {
      fetchPolicy: "cache-and-network",
    },
  },
  link: errorLink.concat(apiLink),
});
