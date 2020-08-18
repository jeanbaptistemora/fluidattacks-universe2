/* eslint-disable fp/no-mutation
  -------
  We need it in order to use methods from xhr and mutate some values from a
  graphQL error response.
*/
import { ApolloClient } from "apollo-client";
import { ApolloProvider as BaseApolloProvider } from "@apollo/react-hooks";
import { ErrorResponse } from "apollo-link-error";
import { Logger } from "./logger";
import React from "react";
import { WebSocketLink } from "apollo-link-ws";
import _ from "lodash";
import { createNetworkStatusNotifier } from "react-apollo-network-status";
import { createUploadLink } from "apollo-upload-client";
import { getEnvironment } from "./environment";
import { getMainDefinition } from "apollo-utilities";
import { msgError } from "./notifications";
import translate from "./translations/translate";
import { useHistory } from "react-router";
import {
  ApolloLink,
  ExecutionResult,
  FetchResult,
  NextLink,
  Observable,
  Operation,
} from "apollo-link";
import {
  FragmentDefinitionNode,
  GraphQLError,
  OperationDefinitionNode,
} from "graphql";
import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ServerError, ServerParseError } from "apollo-link-http-common";

interface IHandledErrorAttr {
  graphQLErrors?: readonly GraphQLError[];
  networkError?: Error | ServerError | ServerParseError;
  skipForwarding?: () => void;
  response?: ExecutionResult;
  operation: Operation;
  forward: NextLink;
}

interface IErrorHandlerAttr {
  // It can return a void type according to apollo-link
  // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
  (error: IHandledErrorAttr): Observable<FetchResult> | void;
}

const getCookie: (name: string) => string = (name: string): string => {
  if (document.cookie !== "") {
    const cookies: string[] = document.cookie.split(";");
    const cookieValue:
      | string
      | undefined = cookies.find((cookie: string): boolean =>
      cookie.trim().startsWith(`${name}=`)
    );
    if (!_.isUndefined(cookieValue)) {
      return decodeURIComponent(cookieValue.trim().substring(name.length + 1));
    }
  }

  return "";
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
interface IExtendedFetchConfig extends RequestInit {
  notifyUploadProgress: boolean;
  onUploadProgress: (ev: ProgressEvent) => void;
}

const xhrWrapper: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string,
  options: IExtendedFetchConfig
): Promise<Response> =>
  new Promise(
    (
      resolve: (value: Response) => void,
      reject: (reason: Error) => void
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
        Object.keys(options.headers).forEach((key: string): void => {
          xhr.setRequestHeader(key, _.get(options.headers, key));
        });
      }

      xhr.upload.onprogress = options.onUploadProgress;

      xhr.send(options.body);
    }
  );

const extendedFetch: WindowOrWorkerGlobalScope["fetch"] = async (
  uri: string,
  options: IExtendedFetchConfig
): Promise<Response> =>
  options.notifyUploadProgress ? xhrWrapper(uri, options) : fetch(uri, options);

const httpLink: ApolloLink = createUploadLink({
  credentials: "same-origin",
  fetch: extendedFetch,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
    accept: "application/json",
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
    const definition:
      | OperationDefinitionNode
      | FragmentDefinitionNode = getMainDefinition(query);

    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  networkStatusNotifier.link.concat(httpLink)
);

/**
 * Custom error link implementation to prevent propagation
 * of handled network errors
 * @see https://github.com/apollographql/react-apollo/issues/1548
 * @see https://github.com/apollographql/apollo-link/issues/855
 */
const onError: (errorHandler: IErrorHandlerAttr) => ApolloLink = (
  errorHandler: IErrorHandlerAttr
): ApolloLink =>
  new ApolloLink(
    (operation: Operation, forward: NextLink): Observable<FetchResult> =>
      new Observable(
        (
          observer: ZenObservable.SubscriptionObserver<FetchResult>
        ): (() => void) => {
          const subscription: ZenObservable.Subscription | undefined = (():
            | ZenObservable.Subscription
            | undefined => {
            try {
              const operationObserver: Observable<FetchResult> = forward(
                operation
              );

              return operationObserver.subscribe({
                complete: observer.complete.bind(observer),
                error: (networkError: ErrorResponse["networkError"]): void => {
                  errorHandler({
                    forward,
                    networkError,
                    operation,
                  });
                },
                next: (result: FetchResult): void => {
                  // It is necessary to change the variable value
                  // eslint-disable-next-line fp/no-let
                  let isForwarded: boolean = true;
                  const skipForwarding: () => void = (): void => {
                    isForwarded = false;
                  };
                  if (result.errors !== undefined) {
                    errorHandler({
                      forward,
                      graphQLErrors: result.errors,
                      operation,
                      response: result,
                      skipForwarding: skipForwarding,
                    });
                  }
                  // isForwarded can change its value
                  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
                  if (isForwarded) {
                    observer.next(result);
                  }
                },
              });
            } catch (exception) {
              errorHandler({
                forward,
                networkError: exception as Error,
                operation,
              });
            }
          })();

          return (): void => {
            if (subscription !== undefined) {
              subscription.unsubscribe();
            }
          };
        }
      )
  );

type History = ReturnType<typeof useHistory>;
// Top-level error handling
const errorLink: (history: History) => ApolloLink = (
  history: History
): ApolloLink =>
  onError(
    ({
      graphQLErrors,
      networkError,
      response,
      skipForwarding,
    }: IHandledErrorAttr): void => {
      if (networkError !== undefined) {
        const { statusCode } = networkError as { statusCode?: number };
        const forbidden: number = 403;

        switch (statusCode) {
          case undefined:
            msgError(translate.t("group_alerts.error_network"), "Offline");
            break;
          case forbidden:
            // Django CSRF expired
            location.reload();
            break;
          default:
            msgError(translate.t("group_alerts.error_textsad"));
            Logger.warning("A network error occurred", { ...networkError });
        }
      } else {
        if (graphQLErrors !== undefined) {
          graphQLErrors.forEach((error: GraphQLError): void => {
            switch (error.message) {
              case "Login required":
              case "Exception - User token has expired":
                if (response !== undefined) {
                  if (_.isFunction(skipForwarding)) {
                    skipForwarding();
                  }
                }
                location.assign("/integrates/logout");
                break;
              case "Access denied":
              case "Exception - Event not found":
              case "Exception - Finding not found":
              case "Exception - Organization name is invalid":
              case "Exception - Project does not exist":
                if (response !== undefined) {
                  if (_.isFunction(skipForwarding)) {
                    skipForwarding();
                  }
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
    }
  );

type ProviderProps = Omit<
  React.ComponentProps<typeof BaseApolloProvider>,
  "client"
>;
export const ApolloProvider: React.FC<ProviderProps> = (
  props: ProviderProps
): JSX.Element => {
  const history: History = useHistory();

  const client: ApolloClient<NormalizedCacheObject> = React.useMemo(
    (): ApolloClient<NormalizedCacheObject> =>
      new ApolloClient({
        cache: new InMemoryCache(),
        connectToDevTools: getEnvironment() !== "production",
        defaultOptions: {
          watchQuery: {
            fetchPolicy: "cache-and-network",
          },
        },
        link: errorLink(history).concat(apiLink),
      }),
    // This computed value will never change
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return React.createElement(BaseApolloProvider, { client, ...props });
};
