import {
  ApolloClient,
  ApolloLink,
  ApolloProvider as BaseApolloProvider,
  createHttpLink,
  FetchResult,
  InMemoryCache,
  NextLink,
  NormalizedCacheObject,
  Observable,
  Operation,
  ServerError,
  ServerParseError,
} from "@apollo/client";
// tslint:disable-next-line: no-submodule-imports
import { setContext } from "@apollo/client/link/context";
// tslint:disable-next-line: no-submodule-imports
import { ErrorResponse } from "@apollo/client/link/error";
import * as SecureStore from "expo-secure-store";
import { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
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
  skipForwarding?(): void;
}

// It can return a void type according to apollo-link
// tslint:disable-next-line:invalid-void
type ErrorHandler = (error: IHandledErrorAttr) => Observable<FetchResult> | void;

type History = ReturnType<typeof useHistory>;

const apiHost: string = getEnvironment().url;

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
        let isForwarded: boolean = true;
        const skipForwarding: () => void = (): void => {
          isForwarded = false;
        };

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

// Top-level error handling
const errorLink: ((history: History) => ApolloLink) = (
  history: History,
): ApolloLink =>
  onError(({ graphQLErrors, networkError, response, skipForwarding }: IHandledErrorAttr): void => {
    if (networkError !== undefined) {
      const { statusCode } = networkError as { statusCode?: number };

      switch (statusCode) {
        case undefined:
          Alert.alert(
            i18next.t("common.networkError.title"),
            i18next.t("common.networkError.msg"));
          break;
        default:
          Alert.alert(
            i18next.t("common.error.title"),
            i18next.t("common.error.msg"));
          LOGGER.warning("A network error occurred", { ...networkError });
      }
    } else {
      if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(async (error: GraphQLError): Promise<void> => {
          if (error.message === "Login required") {
            if (response !== undefined) {
              if (_.isFunction(skipForwarding)) {
                skipForwarding();
              }
            }
            await logout();
            Alert.alert(
              i18next.t("common.sessionExpired.title"),
              i18next.t("common.sessionExpired.msg"));
            history.replace("/Login");
          }
        });
      }
    }
  });

const authLink: ApolloLink = setContext(async (): Promise<Record<string, unknown>> => {
  let token: string;
  try {
    token = await SecureStore.getItemAsync("integrates_session") as string;
  } catch (exception) {
    token = "";
    await SecureStore.deleteItemAsync("integrates_session");
  }

  return {
    headers: {
      authorization: `Bearer ${token}`,
    },
  };
});

const httpLink: ApolloLink = createHttpLink({
  uri: `${apiHost}/api`,
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
    (): ApolloClient<NormalizedCacheObject> => new ApolloClient({
      cache: new InMemoryCache(),
      link: errorLink(history)
        .concat(authLink.concat(httpLink)),
    }),
    []);

  return React.createElement(BaseApolloProvider, { client, ...props });
};

export { apolloProvider as ApolloProvider };
