/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloError } from "@apollo/client";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleEditGroupDataError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error): void => {
    if (error.message === "Exception - This group has active roots") {
      msgError(translate.t("searchFindings.servicesTable.errors.activeRoots"));
    } else if (
      error.message ===
      "Exception - Incorrect change in managed parameter. Please review the payment conditions"
    ) {
      msgError(
        translate.t("searchFindings.servicesTable.errors.invalidManaged")
      );
    } else if (
      error.message ===
      "Exception - The action is not allowed during the free trial"
    ) {
      msgError(translate.t("searchFindings.servicesTable.errors.trial"));
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred editing group services", error);
    }
  });
};

export { handleEditGroupDataError };
