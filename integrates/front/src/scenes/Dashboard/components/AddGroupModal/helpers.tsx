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

const handleCreateError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error invalid group name":
        msgError(translate.t("organization.tabs.groups.newGroup.invalidName"));
        break;
      case "Exception - User is not a member of the target organization":
        msgError(
          translate.t("organization.tabs.groups.newGroup.userNotInOrganization")
        );
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred adding a group", error);
    }
  });
};

const handleUpdateError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error empty value is not valid":
        msgError(translate.t("group.scope.git.errors.invalid"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error(`Couldn't update tours`, error);
    }
  });
};

const getSwitchButtonHandlers = (
  values: {
    squad: boolean;
    machine: boolean;
  },
  setFieldValue: (
    field: string,
    value: unknown,
    shouldValidate?: boolean | undefined
  ) => void,
  scope: "machine" | "squad"
): (() => void) => {
  function handleMachineBtnChange(): void {
    setFieldValue("machine", !values.machine);

    if (values.machine) {
      setFieldValue("squad", false);
    }
  }

  function handleSquadBtnChange(): void {
    setFieldValue("squad", !values.squad);

    if (!values.squad) {
      setFieldValue("machine", true);
    }
  }

  if (scope === "machine") {
    return handleMachineBtnChange;
  }

  return handleSquadBtnChange;
};

export { getSwitchButtonHandlers, handleCreateError, handleUpdateError };
