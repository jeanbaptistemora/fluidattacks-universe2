import type { FetchResult } from "@apollo/client";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import type { useHistory } from "react-router-dom";

import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const getErrors: <Type>(
  results: FetchResult<Type>[]
) => (readonly GraphQLError[])[] = <Type,>(
  results: FetchResult<Type>[]
): (readonly GraphQLError[])[] =>
  results
    .map((result: FetchResult<Type>): readonly GraphQLError[] | undefined =>
      "errors" in result ? result.errors : undefined
    )
    .filter(
      (
        optionalErrors: readonly GraphQLError[] | undefined
      ): optionalErrors is readonly GraphQLError[] =>
        !_.isUndefined(optionalErrors)
    );

const operationObservSubscribeComplete = (
  isForwarded: boolean,
  initialHistoryState: Record<string, unknown> | null,
  observer: ZenObservable.SubscriptionObserver<FetchResult>,
  finalHistoryState: Record<string, unknown> | null
): void => {
  if (isForwarded && initialHistoryState?.key === finalHistoryState?.key) {
    observer.complete.bind(observer)();
  }
};

type History = ReturnType<typeof useHistory>;

const handleGraphQLError = (
  error: GraphQLError,
  history: History,
  skipForwarding: (() => void) | undefined,
  response?: ExecutionResult
): void => {
  switch (error.message) {
    case "Login required":
    case "Exception - User token has expired":
      if (response !== undefined) {
        if (_.isFunction(skipForwarding)) {
          skipForwarding();
        }
      }
      location.assign("/logout");
      break;
    case "Access denied":
    case "Access denied or tag not found":
    case "Exception - Event not found":
    case "Exception - Group does not exist":
      if (response !== undefined) {
        if (_.isFunction(skipForwarding)) {
          skipForwarding();
        }
      }
      msgError(translate.t("groupAlerts.accessDenied"));
      history.replace("/home");
      break;
    default:
    // Propagate
  }
};

export { getErrors, handleGraphQLError, operationObservSubscribeComplete };
