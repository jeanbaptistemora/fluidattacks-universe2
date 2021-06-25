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
    type: string;
    squad: boolean;
    forces: boolean;
    machine: boolean;
  },
  setFieldValue: (
    field: string,
    value: unknown,
    shouldValidate?: boolean | undefined
  ) => void,
  scope: "forces" | "machine" | "squad" | "subscription"
): ((checked: boolean) => void) => {
  function handleSubscriptionTypeChange(): void {
    setFieldValue("machine", values.type !== "CONTINUOUS");
    setFieldValue("squad", true);
    setFieldValue("forces", values.type !== "CONTINUOUS");
  }

  function handleMachineBtnChange(): void {
    setFieldValue("machine", !values.machine);

    if (values.machine) {
      setFieldValue("squad", false);
      setFieldValue("forces", false);
    }
  }

  function handleSquadBtnChange(): void {
    setFieldValue("squad", !values.squad);

    if (!values.squad) {
      setFieldValue("machine", true);
    }
  }

  function handleForcesBtnChange(): void {
    if (values.machine) {
      setFieldValue("forces", !values.forces);
    } else {
      setFieldValue("forces", false);
    }
  }

  if (scope === "subscription") {
    return handleSubscriptionTypeChange;
  } else if (scope === "machine") {
    return handleMachineBtnChange;
  } else if (scope === "squad") {
    return handleSquadBtnChange;
  }

  return handleForcesBtnChange;
};

export {
  handleCreateError,
  handleGroupNameErrorHelper,
  getSwitchButtonHandlers,
};
