/* eslint-disable fp/no-mutation
  -------
  We need it in order to use methods from xhr and mutate some values from a
  graphQL error response.
*/
import {
  ApolloClient,
  ApolloLink,
  ApolloProvider as BaseApolloProvider,
  InMemoryCache,
  Observable,
} from "@apollo/client";
import type {
  FetchResult,
  NextLink,
  NormalizedCacheObject,
  Operation,
  ServerError,
  ServerParseError,
} from "@apollo/client";
import type { ErrorResponse } from "@apollo/client/link/error";
import { RetryLink } from "@apollo/client/link/retry";
import { WebSocketLink } from "@apollo/client/link/ws";
import {
  getMainDefinition,
  relayStylePagination,
} from "@apollo/client/utilities";
import { createUploadLink } from "apollo-upload-client";
import type {
  ExecutionResult,
  FragmentDefinitionNode,
  GraphQLError,
  OperationDefinitionNode,
} from "graphql";
import _ from "lodash";
import { createElement, useMemo } from "react";
import { createNetworkStatusNotifier } from "react-apollo-network-status";
import { useHistory } from "react-router-dom";

import {
  handleGraphQLError,
  operationObservSubscribeComplete,
} from "./helpers";

import { getEnvironment } from "utils/environment";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

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
    const cookieValue: string | undefined = cookies.find(
      (cookie: string): boolean => cookie.trim().startsWith(`${name}=`)
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

const httpLink = createUploadLink({
  credentials: "same-origin",
  fetch: extendedFetch,
  headers: {
    "X-CSRFToken": getCookie("csrftoken"),
    accept: "application/json",
  },
  uri: `${window.location.origin}/api`,
});

const wsLink: ApolloLink = new WebSocketLink({
  options: {
    lazy: true,
    reconnect: true,
  },
  uri: `wss://${window.location.host}/api`,
});

const apiLink: ApolloLink = ApolloLink.split(
  ({ query }: Operation): boolean => {
    const definition: FragmentDefinitionNode | OperationDefinitionNode =
      getMainDefinition(query);

    return (
      definition.kind === "OperationDefinition" &&
      definition.operation === "subscription"
    );
  },
  wsLink,
  httpLink
);

const { link: networkStatusLink, useApolloNetworkStatus } =
  createNetworkStatusNotifier();

const retryLink: ApolloLink = new RetryLink({
  attempts: {
    max: 5,
    retryIf: (error: unknown): boolean => error !== undefined,
  },
  delay: {
    initial: 300,
    jitter: true,
    max: Infinity,
  },
});

/**
 * Custom error link implementation to prevent propagation
 * of handled network errors
 * @see https://github.com/apollographql/react-apollo/issues/1548
 * @see https://github.com/apollographql/apollo-link/issues/855
 */
const onError: (
  errorHandler: IErrorHandlerAttr,
  history: History
) => ApolloLink = (errorHandler: IErrorHandlerAttr): ApolloLink =>
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
              const operationObserver: Observable<FetchResult> =
                forward(operation);
              // It is necessary to change the variable value
              // eslint-disable-next-line fp/no-let
              let isForwarded: boolean = true;
              const skipForwarding: () => void = (): void => {
                isForwarded = false;
              };
              const initialHistoryState: Record<string, unknown> | null =
                history.state;

              return operationObserver.subscribe({
                complete: (): void => {
                  const finalHistoryState: Record<string, unknown> | null =
                    history.state;
                  operationObservSubscribeComplete(
                    isForwarded,
                    initialHistoryState,
                    observer,
                    finalHistoryState
                  );
                },
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
                      skipForwarding,
                    });
                  }
                  // IsForwarded can change its value
                  // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
                  if (isForwarded) {
                    observer.next(result);
                  }
                },
              });
            } catch (exception: unknown) {
              errorHandler({
                forward,
                networkError: exception as Error,
                operation,
              });

              return undefined;
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
            msgError(translate.t("groupAlerts.errorNetwork"), "Offline");
            break;
          case forbidden:
            // Django CSRF expired
            location.reload();
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("A network error occurred", { ...networkError });
        }
      } else if (graphQLErrors !== undefined) {
        graphQLErrors.forEach((error: GraphQLError): void => {
          handleGraphQLError(error, history, skipForwarding, response);
        });
      }
    },
    history
  );

/**
 * Load cache with union type definitions
 * @see https://www.apollographql.com/docs/react/v2.6/data/fragments/#fragments-on-unions-and-interfaces
 */
const getCache: () => InMemoryCache = (): InMemoryCache =>
  new InMemoryCache({
    possibleTypes: {
      Root: ["GitRoot", "IPRoot", "URLRoot"],
    },
    typePolicies: {
      Group: {
        fields: {
          toeInputs: relayStylePagination(),
          toeLines: relayStylePagination(),
        },
        keyFields: ["name"],
      },
      Me: { keyFields: ["userEmail"] },
      Organization: { keyFields: ["name"] },
    },
  });

type ProviderProps = Omit<
  React.ComponentProps<typeof BaseApolloProvider>,
  "client"
>;
const ApolloProvider: React.FC<ProviderProps> = (
  props: ProviderProps
): JSX.Element => {
  const history: History = useHistory();
  const client: ApolloClient<NormalizedCacheObject> = useMemo(
    (): ApolloClient<NormalizedCacheObject> =>
      new ApolloClient({
        cache: getCache(),
        connectToDevTools: getEnvironment() !== "production",
        defaultOptions: {
          watchQuery: {
            fetchPolicy: "cache-and-network",
          },
        },
        link: ApolloLink.from([
          errorLink(history),
          networkStatusLink,
          retryLink,
          apiLink,
        ]),
      }),
    // This computed value will never change
    // eslint-disable-next-line react-hooks/exhaustive-deps
    []
  );

  return createElement(BaseApolloProvider, { client, ...props });
};

export { getCache, useApolloNetworkStatus, ApolloProvider };
