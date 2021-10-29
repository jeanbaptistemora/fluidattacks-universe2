import {
  ApolloClient,
  ApolloLink,
  ApolloProvider as BaseApolloProvider,
  InMemoryCache,
  Observable,
  createHttpLink,
} from "@apollo/client";
import type {
  FetchResult,
  NextLink,
  NormalizedCacheObject,
  Operation,
  ServerError,
  ServerParseError,
} from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import type { ErrorResponse } from "@apollo/client/link/error";
import { RetryLink } from "@apollo/client/link/retry";
import { deleteItemAsync, getItemAsync } from "expo-secure-store";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import { createElement, useMemo } from "react";
import type React from "react";
import { Alert, NativeModules } from "react-native";
import type { ReactNativeSSLPinning } from "react-native-ssl-pinning";
import { fetch as sslPinningFetch } from "react-native-ssl-pinning";
import { useHistory } from "react-router-native";

import { getEnvironment } from "./environment";
import { LOGGER } from "./logger";
import { useSessionToken } from "./sessionToken/context";
import { logout } from "./socialAuth";
import { i18next } from "./translations/translate";

/**
 * Handled error attributes
 */
interface IHandledErrorAttr {
  forward: NextLink;
  graphQLErrors?: readonly GraphQLError[];
  networkError?: Error | ServerError | ServerParseError;
  operation: Operation;
  response?: ExecutionResult;
  skipForwarding?: () => void;
}

/*
 * It can return a void type according to apollo-link
 */
// eslint-disable-next-line @typescript-eslint/no-type-alias
type ErrorHandler = (
  error: IHandledErrorAttr
  // eslint-disable-next-line @typescript-eslint/no-invalid-void-type
) => Observable<FetchResult> | void;

type History = ReturnType<typeof useHistory>;

const apiHost: string = getEnvironment().url;

/**
 * Custom error link implementation to prevent propagation
 * of handled network errors
 * @see https://github.com/apollographql/react-apollo/issues/1548
 * @see https://github.com/apollographql/apollo-link/issues/855
 */
const onError: (errorHandler: ErrorHandler) => ApolloLink = (
  errorHandler: ErrorHandler
): ApolloLink =>
  new ApolloLink(
    (operation: Operation, forward: NextLink): Observable<FetchResult> =>
      new Observable(
        (
          observer: ZenObservable.SubscriptionObserver<FetchResult>
        ): (() => void) => {
          // eslint-disable-next-line fp/no-let, @typescript-eslint/init-declarations
          let subscription: ZenObservable.Subscription | undefined;

          try {
            const operationObserver: Observable<FetchResult> =
              forward(operation);
            // eslint-disable-next-line fp/no-let
            let isForwarded: boolean = true;
            const skipForwarding: () => void = (): void => {
              // eslint-disable-next-line fp/no-mutation
              isForwarded = false;
            };

            // eslint-disable-next-line fp/no-mutation
            subscription = operationObserver.subscribe({
              complete: (): void => {
                if (isForwarded) {
                  observer.complete.bind(observer)();
                }
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
          }

          return (): void => {
            if (subscription !== undefined) {
              subscription.unsubscribe();
            }
          };
        }
      )
  );

const statusCodeAlert = (
  networkError: Error | ServerError | ServerParseError | undefined
): void => {
  const { statusCode } = networkError as { statusCode?: number };
  switch (statusCode) {
    case undefined:
      Alert.alert(
        i18next.t("common.networkError.title"),
        i18next.t("common.networkError.msg")
      );
      break;
    default:
      Alert.alert(
        i18next.t("common.error.title"),
        i18next.t("common.error.msg")
      );
      LOGGER.warning("A network error occurred", { ...networkError });
  }
};

// Top-level error handling
const errorLink: (
  history: History,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
) => ApolloLink = (
  history: History,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
): ApolloLink =>
  onError(
    ({
      graphQLErrors,
      networkError,
      response,
      skipForwarding,
    }: IHandledErrorAttr): void => {
      if (networkError !== undefined) {
        statusCodeAlert(networkError);
      } else if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(
          // eslint-disable-next-line @typescript-eslint/no-misused-promises
          async (error: GraphQLError): Promise<void> => {
            if (error.message === "Login required") {
              if (response !== undefined) {
                if (_.isFunction(skipForwarding)) {
                  skipForwarding();
                }
              }
              await logout(setSessionToken);
              Alert.alert(
                i18next.t("common.sessionExpired.title"),
                i18next.t("common.sessionExpired.msg")
              );
              history.replace("/Login");
            }
          }
        );
      }
    }
  );

const getToken: (
  sessionToken: string,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
) => Promise<string> = async (
  sessionToken: string,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
): Promise<string> => {
  const key = "session_token";

  if (!_.isEmpty(sessionToken)) {
    return sessionToken;
  }

  try {
    const token = await getItemAsync(key);
    setSessionToken(token === null ? "" : token);

    return token === null ? "" : token;
  } catch (exception: unknown) {
    await deleteItemAsync(key);

    return "";
  }
};

const authLink: (
  sessionToken: string,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
) => ApolloLink = (
  sessionToken: string,
  setSessionToken: React.Dispatch<React.SetStateAction<string>>
): ApolloLink =>
  setContext(async (): Promise<Record<string, unknown>> => {
    const token = await getToken(sessionToken, setSessionToken);

    return {
      headers: {
        authorization: `Bearer ${token}`,
      },
    };
  });

interface ISecureFetchOptions extends RequestInit {
  pkPinning: ReactNativeSSLPinning.Options["pkPinning"];
  sslPinning: ReactNativeSSLPinning.Options["sslPinning"];
}

const extendedFetch = async (
  input: string,
  init?: RequestInit | undefined
): Promise<Response> => {
  if (NativeModules.RNSslPinning !== null) {
    const secureFetch = sslPinningFetch as unknown as (
      url: string,
      options: ISecureFetchOptions
    ) => Promise<Response>;

    return secureFetch(input, {
      ...init,
      pkPinning: true,
      sslPinning: {
        certs: ["sha256/__PINNED_PK__"],
      },
    });
  }

  return fetch(input, init);
};

const apiLink: ApolloLink = createHttpLink({
  fetch: extendedFetch,
  uri: `${apiHost}/api`,
});

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

type ProviderProps = Omit<
  React.ComponentProps<typeof BaseApolloProvider>,
  "client"
>;
const ApolloProvider: React.FC<ProviderProps> = (
  props: ProviderProps
): JSX.Element => {
  const history: History = useHistory();
  const [sessionToken, setSessionToken] = useSessionToken();
  const client: ApolloClient<NormalizedCacheObject> = useMemo(
    (): ApolloClient<NormalizedCacheObject> =>
      new ApolloClient({
        cache: new InMemoryCache(),
        link: ApolloLink.from([
          errorLink(history, setSessionToken),
          retryLink,
          authLink(sessionToken, setSessionToken),
          apiLink,
        ]),
      }),
    [history, sessionToken, setSessionToken]
  );

  return createElement(BaseApolloProvider, { client, ...props });
};

export { ApolloProvider };
