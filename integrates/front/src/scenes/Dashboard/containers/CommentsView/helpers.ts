/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

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
    switch (message) {
      case "Exception - Invalid field length in form":
        msgError(translate.t("validations.invalidFieldLength"));
        break;
      case "Exception - Comment parent is invalid":
        msgError(
          translate.t("validations.invalidCommentParent", {
            count: 1,
          })
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(`An error occurred posting ${type}`, addCommentError);
    }
  });
};

export { handleAddCommentErrorHelper };
