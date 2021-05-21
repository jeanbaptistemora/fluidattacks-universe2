import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleAddCommentErrorHelper = (
  addCommentError: ApolloError,
  type: string
): void => {
  addCommentError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    if (message === "Exception - Comment parent is invalid") {
      msgError(
        translate.t("validations.invalidCommentParent", {
          count: 1,
        })
      );
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning(`An error occurred posting ${type}`, addCommentError);
    }
  });
};

export { handleAddCommentErrorHelper };
