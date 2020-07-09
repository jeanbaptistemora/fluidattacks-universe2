import { ApolloProvider as BaseApolloProvider } from "@apollo/react-hooks";
import { InMemoryCache, NormalizedCacheObject } from "apollo-cache-inmemory";
import { ApolloClient } from "apollo-client";
import {
  ApolloLink,
  FetchResult,
  NextLink,
  Observable,
  Operation,
} from "apollo-link";
import { setContext } from "apollo-link-context";
import { ErrorHandler, ErrorResponse } from "apollo-link-error";
import { createHttpLink } from "apollo-link-http";
import * as SecureStore from "expo-secure-store";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Alert } from "react-native";
import { useHistory } from "react-router-native";

import { getEnvironment } from "./environment";
import { rollbar } from "./rollbar";
import { logout } from "./socialAuth";
import { i18next } from "./translations/translate";

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

// Top-level error handling
const errorLink: ((history: History) => ApolloLink) = (
  history: History,
): ApolloLink =>
  onError(({ graphQLErrors, networkError, response }: ErrorResponse): void => {
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
          rollbar.error("A network error occurred", { ...networkError });
      }
    } else {
      if (graphQLErrors !== undefined) {
        graphQLErrors.forEach(async (error: GraphQLError): Promise<void> => {
          if (error.message === "Login required") {
            if (response !== undefined) {
              response.data = undefined;
              response.errors = [];
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

const authLink: ApolloLink = setContext(async (): Promise<Dictionary> => {
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
  uri: `${apiHost}/integrates/api`,
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
