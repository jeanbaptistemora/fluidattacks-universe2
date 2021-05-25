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
    drills: boolean;
    forces: boolean;
    skims: boolean;
  },
  setFieldValue: (
    field: string,
    value: unknown,
    shouldValidate?: boolean | undefined
  ) => void,
  scope: "drills" | "forces" | "skims" | "subscription"
): ((checked: boolean) => void) => {
  function handleSubscriptionTypeChange(): void {
    setFieldValue("skims", values.type !== "CONTINUOUS");
    setFieldValue("drills", true);
    setFieldValue("forces", values.type !== "CONTINUOUS");
  }

  function handleSkimsBtnChange(): void {
    setFieldValue("skims", !values.skims);

    if (values.skims) {
      setFieldValue("drills", false);
      setFieldValue("forces", false);
    }
  }

  function handleDrillsBtnChange(): void {
    setFieldValue("drills", !values.drills);

    if (values.drills) {
      setFieldValue("forces", false);
    } else {
      setFieldValue("skims", true);
    }
  }

  function handleForcesBtnChange(): void {
    if (values.drills) {
      setFieldValue("forces", !values.forces);
    } else {
      setFieldValue("forces", false);
    }
  }

  if (scope === "subscription") {
    return handleSubscriptionTypeChange;
  } else if (scope === "skims") {
    return handleSkimsBtnChange;
  } else if (scope === "drills") {
    return handleDrillsBtnChange;
  }

  return handleForcesBtnChange;
};

export {
  handleCreateError,
  handleGroupNameErrorHelper,
  getSwitchButtonHandlers,
};
