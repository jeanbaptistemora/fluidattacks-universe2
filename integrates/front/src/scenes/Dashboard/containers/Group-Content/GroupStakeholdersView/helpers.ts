import type { ApolloError, ObservableQuery } from "@apollo/client";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";

import type {
  IRemoveStakeholderAttr,
  IStakeholderAttrs,
} from "scenes/Dashboard/containers/Group-Content/GroupStakeholdersView/types";
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
      case "Exception - The previous invitation to this user was requested" +
        " less than a minute ago":
        msgError(translate.t("validations.requestedTooSoon"));
        break;
      case "Exception - Invalid field in form":
        msgError(translate.t("validations.invalidValueInField"));
        break;
      case "Exception - Invalid field length in form":
        msgError(translate.t("validations.invalidFieldLength"));
        break;
      case "Exception - Invalid characters":
        msgError(translate.t("validations.invalidChar"));
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
      case "Exception - The stakeholder has been granted access to the organization previously":
        msgError(translate.t("validations.stakeholderHasOrganizationAccess"));
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

type IRemoveResult = ExecutionResult<IRemoveStakeholderAttr>;

const removeMultipleAccess = async (
  removeStakeholderAccess: (
    variables: Record<string, unknown>
  ) => Promise<IRemoveResult>,
  stakeholders: IStakeholderAttrs[],
  groupName: string
): Promise<IRemoveResult[]> => {
  const chunkSize = 5;
  const stakeholderChunks = _.chunk(stakeholders, chunkSize);
  const removeChunks = stakeholderChunks.map(
    (chunk): (() => Promise<IRemoveResult[]>) =>
      async (): Promise<IRemoveResult[]> => {
        const updates = chunk.map(
          async (stakeholder): Promise<IRemoveResult> =>
            removeStakeholderAccess({
              variables: {
                groupName,
                userEmail: stakeholder.email,
              },
            })
        );

        return Promise.all(updates);
      }
  );

  return removeChunks.reduce(
    async (previousValue, currentValue): Promise<IRemoveResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<IRemoveResult[]>([])
  );
};

const getAreAllMutationValid = (results: IRemoveResult[]): boolean[] => {
  return results.map((result: IRemoveResult): boolean => {
    if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
      const removeInfoSuccess: boolean = _.isUndefined(
        result.data.removeStakeholderAccess
      )
        ? true
        : result.data.removeStakeholderAccess.success;

      return removeInfoSuccess;
    }

    return false;
  });
};

export {
  getAreAllMutationValid,
  handleGrantError,
  handleEditError,
  removeMultipleAccess,
};
