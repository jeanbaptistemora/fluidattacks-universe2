import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleCreateError = ({ graphQLErrors }: ApolloError): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - There are no group names available at the moment":
        msgError(translate.t("organization.tabs.groups.newGroup.noGroupName"));
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

function handleGroupNameErrorHelper(
  graphQLErrors: readonly GraphQLError[]
): void {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (
      error.message ===
      "Exception - There are no group names available at the moment"
    ) {
      msgError(translate.t("organization.tabs.groups.newGroup.noGroupName"));
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred adding access token", error);
    }
  });
}

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

export {
  handleCreateError,
  handleGroupNameErrorHelper,
  getSwitchButtonHandlers,
};
