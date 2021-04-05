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
import type React from "react";
import { createElement, useMemo } from "react";
import { Alert } from "react-native";
import { useHistory } from "react-router-native";

import { getEnvironment } from "./environment";
import { LOGGER } from "./logger";
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
            const operationObserver: Observable<FetchResult> = forward(
              operation
            );
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
              await logout();
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

const authLink: ApolloLink = setContext(
  async (): Promise<Record<string, unknown>> => {
    try {
      const token: string = (await getItemAsync(
        "integrates_session"
      )) as string;

      return {
        headers: {
          authorization: `Bearer ${token}`,
        },
      };
    } catch (exception: unknown) {
      const token: string = "";
      await deleteItemAsync("integrates_session");

      return {
        headers: {
          authorization: `Bearer ${token}`,
        },
      };
    }
  }
);

const apiLink: ApolloLink = createHttpLink({
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
  const client: ApolloClient<NormalizedCacheObject> = useMemo(
    (): ApolloClient<NormalizedCacheObject> =>
      new ApolloClient({
        cache: new InMemoryCache(),
        link: ApolloLink.from([
          errorLink(history),
          retryLink,
          authLink,
          apiLink,
        ]),
      }),
    [history]
  );

  return createElement(BaseApolloProvider, { client, ...props });
};

export { ApolloProvider };
