/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type {
  ApolloError,
  FetchResult,
  MutationFunctionOptions,
  MutationHookOptions,
} from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";

import { GET_FINDING_HEADER } from "../../FindingContent/queries";
import { GET_FINDING_LOCATIONS } from "../../GroupFindingsView/loaders/VulnerabilitiesLoader/queries";
import type { IVulnerabilitiesAttr } from "../types";
import {
  getRequestedZeroRiskVulns,
  getVulnsPendingOfAcceptance,
} from "../utils";
import type {
  IConfirmVulnZeroRiskResultAttr,
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/types";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const onTreatmentChangeHelper = (
  isAcceptedUndefinedSelected: boolean,
  vulns: IVulnerabilitiesAttr[],
  setAcceptanceVulns: (pendingVulnsToHandleAcceptance: IVulnDataAttr[]) => void,
  isConfirmRejectZeroRiskSelected: boolean
): void => {
  if (isAcceptedUndefinedSelected) {
    const pendingVulnsToHandleAcceptance: IVulnDataAttr[] =
      getVulnsPendingOfAcceptance(vulns);
    setAcceptanceVulns(pendingVulnsToHandleAcceptance);
  } else if (isConfirmRejectZeroRiskSelected) {
    const requestedZeroRiskVulns: IVulnDataAttr[] =
      getRequestedZeroRiskVulns(vulns);
    setAcceptanceVulns([...requestedZeroRiskVulns]);
  } else {
    setAcceptanceVulns([]);
  }
};

const acceptanceProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IHandleVulnerabilitiesAcceptanceResultAttr): void => {
      if (data.handleVulnerabilitiesAcceptance.success) {
        msgSuccess(
          translate.t("searchFindings.tabVuln.alerts.acceptanceSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - It cant handle acceptance without being requested":
            msgError(
              translate.t(
                "searchFindings.tabVuln.alerts.acceptanceNotRequested"
              )
            );
            break;
          case "Exception - Vulnerability not found":
            msgError(translate.t("groupAlerts.noFound"));
            break;
          case "Exception - Invalid characters":
            msgError(translate.t("validations.invalidChar"));
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred handling acceptance", error);
        }
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId,
        },
      },
    ],
  };
};

const confirmZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId: string,
  groupName: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IConfirmVulnZeroRiskResultAttr): void => {
      if (data.confirmVulnerabilitiesZeroRisk.success) {
        msgSuccess(
          translate.t("groupAlerts.confirmedZeroRiskSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Zero risk vulnerability is not requested"
        ) {
          msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred confirming zero risk vuln", error);
        }
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_HEADER,
        variables: {
          findingId,
        },
      },
    ],
  };
};

const rejectZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId: string,
  groupName: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IRejectZeroRiskVulnResultAttr): void => {
      if (data.rejectVulnerabilitiesZeroRisk.success) {
        msgSuccess(
          translate.t("groupAlerts.rejectedZeroRiskSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (
          error.message ===
          "Exception - Zero risk vulnerability is not requested"
        ) {
          msgError(translate.t("groupAlerts.zeroRiskIsNotRequested"));
        } else {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning("An error occurred rejecting zero risk vuln", error);
        }
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_AND_GROUP_INFO,
        variables: {
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_HEADER,
        variables: {
          findingId,
        },
      },
      {
        query: GET_FINDING_LOCATIONS,
        variables: {
          findingId,
        },
      },
    ],
  };
};

const isAcceptedUndefinedSelectedHelper = (
  isAcceptedUndefinedSelected: boolean,
  handleAcceptance: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  acceptedVulnIds: string[],
  findingId: string,
  values: {
    justification: string;
  },
  rejectedVulnIds: string[]
): void => {
  if (isAcceptedUndefinedSelected) {
    const chunksize = 10;

    if (!_.isEmpty(acceptedVulnIds)) {
      const acceptedChunks = _.chunk(acceptedVulnIds, chunksize);
      acceptedChunks.map(async (acceptedChunk): Promise<void> => {
        await handleAcceptance({
          variables: {
            acceptedVulnerabilities: acceptedChunk,
            findingId,
            justification: values.justification,
            rejectedVulnerabilities: [],
          },
        });
      });
    }
    if (!_.isEmpty(rejectedVulnIds)) {
      const rejectedChunks = _.chunk(rejectedVulnIds, chunksize);
      rejectedChunks.map(async (rejectedChunk): Promise<void> => {
        await handleAcceptance({
          variables: {
            acceptedVulnerabilities: [],
            findingId,
            justification: values.justification,
            rejectedVulnerabilities: rejectedChunk,
          },
        });
      });
    }
  }
};

const isConfirmZeroRiskSelectedHelper = async (
  existAcceptedVulns: boolean,
  isConfirmZeroRiskSelected: boolean,
  confirmZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  acceptedVulnIds: string[],
  findingId: string,
  values: {
    justification: string;
  }
): Promise<void> => {
  if (isConfirmZeroRiskSelected && existAcceptedVulns) {
    await confirmZeroRisk({
      variables: {
        findingId,
        justification: values.justification,
        vulnerabilities: acceptedVulnIds,
      },
    });
  }
};

const isRejectZeroRiskSelectedHelper = async (
  existRejectedVulns: boolean,
  isRejectZeroRiskSelected: boolean,
  rejectZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  findingId: string,
  values: {
    justification: string;
  },
  rejectedVulnIds: string[]
): Promise<void> => {
  if (isRejectZeroRiskSelected && existRejectedVulns) {
    await rejectZeroRisk({
      variables: {
        findingId,
        justification: values.justification,
        vulnerabilities: rejectedVulnIds,
      },
    });
  }
};

export {
  acceptanceProps,
  confirmZeroRiskProps,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  onTreatmentChangeHelper,
  rejectZeroRiskProps,
};
