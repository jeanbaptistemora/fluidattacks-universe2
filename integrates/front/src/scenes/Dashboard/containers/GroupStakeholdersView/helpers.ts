import type { ApolloError, ObservableQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";

import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleGrantError = (grantError: ApolloError): void => {
  grantError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Email is not valid":
        msgError(translate.t("validations.email"));
        break;
      case "Exception - This role can only be granted to Fluid Attacks users":
        msgError(translate.t("validations.userIsNotFromFluidAttacks"));
        break;
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - Invalid phone number in form":
        msgError(translate.t("validations.invalidPhoneNumberInField"));
        break;
      case "Exception - Invalid email address in form":
        msgError(translate.t("validations.invalidEmailInField"));
        break;
      case "Exception - Groups without an active Fluid Attacks service " +
        "can not have Fluid Attacks staff":
        msgError(
          translate.t("validations.fluidAttacksStaffWithoutFluidAttacksService")
        );
        break;
      case "Exception - Groups with any active Fluid Attacks service " +
        "can only have Hackers provided by Fluid Attacks":
        msgError(
          translate.t("validations.noFluidAttacksHackersInFluidAttacksService")
        );
        break;
      case "Exception - The stakeholder has been granted access to the group previously":
        msgError(translate.t("validations.stakeholderHasGroupAccess"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning(
          "An error occurred while adding a stakeholder to the group",
          grantError
        );
    }
  });
};

const handleEditError = (
  editError: ApolloError,
  refetch: ObservableQuery["refetch"]
): void => {
  editError.graphQLErrors.forEach(({ message }: GraphQLError): void => {
    switch (message) {
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
        break;
      case "Exception - This role can only be granted to Fluid Attacks users":
        msgError(translate.t("validations.userIsNotFromFluidAttacks"));
        break;
      case "Exception - Invalid phone number in form":
        msgError(translate.t("validations.invalidPhoneNumberInField"));
        break;
      case "Exception - Groups without an active Fluid Attacks service " +
        "can not have Fluid Attacks staff":
        msgError(
          translate.t("validations.fluidAttacksStaffWithoutFluidAttacksService")
        );
        break;
      case "Exception - Groups with any active Fluid Attacks service " +
        "can only have Hackers provided by Fluid Attacks":
        msgError(
          translate.t("validations.noFluidAttacksHackersInFluidAttacksService")
        );
        break;
      case "Access denied or stakeholder not found":
        msgError(translate.t("groupAlerts.expiredInvitation"));
        void refetch();
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred editing user", editError);
    }
  });
};

export { handleGrantError, handleEditError };
