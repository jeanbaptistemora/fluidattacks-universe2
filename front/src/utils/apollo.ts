import { ApolloProvider as BaseApolloProvider } from "@apollo/react-hooks";
import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient, ApolloError } from "apollo-client";
import { ApolloLink, FetchResult, NextLink, Observable, Operation } from "apollo-link";
import { ErrorHandler, ErrorResponse } from "apollo-link-error";
import { WebSocketLink } from "apollo-link-ws";
import { createUploadLink } from "apollo-upload-client";
import { getMainDefinition } from "apollo-utilities";
import { FragmentDefinitionNode, GraphQLError, OperationDefinitionNode } from "graphql";
import _ from "lodash";
import React from "react";
import { createNetworkStatusNotifier } from "react-apollo-network-status";
import { useHistory } from "react-router";
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
): Promise<Response> => options.notifyUploadProgress
    ? xhrWrapper(uri, options)
    : fetch(uri, options);

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

/**
 * Custom error link implementation to prevent propagation
 * of handled network errors
 * @see https://github.com/apollographql/react-apollo/issues/1548
 * @see https://github.com/apollographql/apollo-link/issues/855
 */
const onError: ((errorHandler: ErrorHandler) => ApolloLink) = (
  errorHandler: ErrorHandler,
): ApolloLink =>
  new ApolloLink((
    operation: Operation,
    forward: NextLink,
  ): Observable<FetchResult> =>
    new Observable((
      observer: ZenObservable.SubscriptionObserver<FetchResult>,
    ): (() => void) => {
      let subscription: ZenObservable.Subscription | undefined;

      try {
        const operationObserver: Observable<FetchResult> = forward(operation);

        subscription = operationObserver.subscribe({
          complete: observer.complete.bind(observer),
          error: (networkError: ErrorResponse["networkError"]): void => {
            errorHandler({
              forward,
              networkError,
              operation,
            });
          },
          next: (result: FetchResult): void => {
            if (result.errors !== undefined) {
              errorHandler({
                forward,
                graphQLErrors: result.errors,
                operation,
                response: result,
              });
            }
            observer.next(result);
          },
        });
      } catch (exception) {
        errorHandler({
          forward,
          networkError: exception as Error,
          operation,
        });
      }

      return (): void => {
        if (subscription !== undefined) {
          subscription.unsubscribe();
        }
      };
    }),
  );

type History = ReturnType<typeof useHistory>;
// Top-level error handling
const errorLink: ((history: History) => ApolloLink) = (
  history: History,
): ApolloLink =>
  onError(({ graphQLErrors, networkError, response }: ErrorResponse): void => {
    if (networkError !== undefined) {
      const { statusCode } = networkError as { statusCode?: number };

      switch (statusCode) {
        case undefined:
          msgError(translate.t("group_alerts.error_network"), "Offline");
          break;
        case 403:
          // Django CSRF expired
          location.reload();
          break;
        default:
          msgError(translate.t("group_alerts.error_textsad"));
          rollbar.error("A network error occurred", { ...networkError });
      }
    } else {
      if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(async (error: GraphQLError): Promise<void> => {
          switch (error.message) {
            case "Login required":
            case "Exception - User token has expired":
              if (response !== undefined) {
                response.data = undefined;
                response.errors = [];
              }
              location.assign("/integrates/logout");
              break;
            case "Access denied":
            case "Exception - Event not found":
            case "Exception - Finding not found":
            case "Exception - Project does not exist":
              if (response !== undefined) {
                response.data = undefined;
                response.errors = [];
              }
              msgError(translate.t("group_alerts.access_denied"));
              history.replace("/home");
              break;
            default:
            // Propagate
          }
        });
      }
    }
  });

type ProviderProps = Omit<
  React.ComponentProps<typeof BaseApolloProvider>,
  "client"
>;
const apolloProvider: React.FC<ProviderProps> = (
  props: ProviderProps,
): JSX.Element => {
  const history: History = useHistory();
  const client: ApolloClient<NormalizedCacheObject> = React.useMemo(
    () => new ApolloClient({
      cache: new InMemoryCache(),
      connectToDevTools: getEnvironment() !== "production",
      defaultOptions: {
        watchQuery: {
          fetchPolicy: "cache-and-network",
        },
      },
      link: errorLink(history)
        .concat(apiLink),
    }),
    []);

  return React.createElement(BaseApolloProvider, { client, ...props });
};

export { apolloProvider as ApolloProvider };
