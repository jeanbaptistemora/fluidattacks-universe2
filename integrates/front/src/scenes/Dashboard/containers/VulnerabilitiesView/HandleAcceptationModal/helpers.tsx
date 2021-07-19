/* eslint @typescript-eslint/no-explicit-any:0 */
import type {
  ApolloCache,
  ApolloError,
  DefaultContext,
  FetchResult,
  MutationFunctionOptions,
  MutationHookOptions,
  OperationVariables,
} from "@apollo/client";
import type { GraphQLError } from "graphql";

import { GET_FINDING_HEADER } from "../../FindingContent/queries";
import type { IVulnerabilitiesAttr } from "../types";
import {
  getRequestedZeroRiskVulns,
  getVulnsPendingOfAcceptation,
} from "../utils";
import type {
  IConfirmZeroRiskVulnResultAttr,
  IHandleVulnerabilitiesAcceptationResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { GET_FINDING_VULN_INFO } from "scenes/Dashboard/containers/VulnerabilitiesView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const onTreatmentChangeHelper = (
  isAcceptedUndefinedSelected: boolean,
  vulns: IVulnerabilitiesAttr[],
  setAcceptationVulns: (
    pendingVulnsToHandleAcceptation: IVulnDataAttr[]
  ) => void,
  isConfirmZeroRiskSelected: boolean,
  isRejectZeroRiskSelected: boolean
): void => {
  if (isAcceptedUndefinedSelected) {
    const pendingVulnsToHandleAcceptation: IVulnDataAttr[] =
      getVulnsPendingOfAcceptation(vulns);
    setAcceptationVulns(pendingVulnsToHandleAcceptation);
  } else if (isConfirmZeroRiskSelected || isRejectZeroRiskSelected) {
    const requestedZeroRiskVulns: IVulnDataAttr[] =
      getRequestedZeroRiskVulns(vulns);
    setAcceptationVulns([...requestedZeroRiskVulns]);
  } else {
    setAcceptationVulns([]);
  }
};

const acceptationProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  canRetrieveAnalyst: boolean,
  canRetrieveZeroRisk: boolean,
  findingId: string,
  groupName: string
): MutationHookOptions => {
  return {
    onCompleted: (data: IHandleVulnerabilitiesAcceptationResultAttr): void => {
      if (data.handleVulnerabilitiesAcceptation.success) {
        msgSuccess(
          translate.t("searchFindings.tabVuln.alerts.acceptationSuccess"),
          translate.t("groupAlerts.updatedTitle")
        );
        refetchData();
        handleCloseModal();
      }
    },
    onError: (errors: ApolloError): void => {
      errors.graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - It cant handle acceptation without being requested":
            msgError(
              translate.t(
                "searchFindings.tabVuln.alerts.acceptationNotRequested"
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
            Logger.warning("An error occurred handling acceptation", error);
        }
      });
    },
    refetchQueries: [
      {
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          canRetrieveZeroRisk,
          findingId,
          groupName,
        },
      },
    ],
  };
};

const confirmZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  canRetrieveAnalyst: boolean,
  canRetrieveZeroRisk: boolean,
  findingId: string,
  groupName: string,
  canGetHistoricState: boolean
): MutationHookOptions => {
  return {
    onCompleted: (data: IConfirmZeroRiskVulnResultAttr): void => {
      if (data.confirmZeroRiskVuln.success) {
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
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          canRetrieveZeroRisk,
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_HEADER,
        variables: {
          canGetHistoricState,
          findingId,
        },
      },
    ],
  };
};

const rejectZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  canRetrieveAnalyst: boolean,
  canRetrieveZeroRisk: boolean,
  findingId: string,
  groupName: string,
  canGetHistoricState: boolean
): MutationHookOptions => {
  return {
    onCompleted: (data: IRejectZeroRiskVulnResultAttr): void => {
      if (data.rejectZeroRiskVuln.success) {
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
        query: GET_FINDING_VULN_INFO,
        variables: {
          canRetrieveAnalyst,
          canRetrieveZeroRisk,
          findingId,
          groupName,
        },
      },
      {
        query: GET_FINDING_HEADER,
        variables: {
          canGetHistoricState,
          findingId,
        },
      },
    ],
  };
};

const isAcceptedUndefinedSelectedHelper = (
  isAcceptedUndefinedSelected: boolean,
  handleAcceptation: (
    options?:
      | MutationFunctionOptions<
          any,
          OperationVariables,
          DefaultContext,
          ApolloCache<any>
        >
      | undefined
  ) => Promise<FetchResult>,
  acceptedVulnIds: string[],
  findingId: string,
  values: {
    justification: string;
  },
  rejectedVulnIds: string[]
): void => {
  if (isAcceptedUndefinedSelected) {
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void handleAcceptation({ //NOSONAR
      variables: {
        acceptedVulns: acceptedVulnIds,
        findingId,
        justification: values.justification,
        rejectedVulns: rejectedVulnIds,
      },
    });
  }
};

const isConfirmZeroRiskSelectedHelper = (
  isConfirmZeroRiskSelected: boolean,
  confirmZeroRisk: (
    options?:
      | MutationFunctionOptions<
          any,
          OperationVariables,
          DefaultContext,
          ApolloCache<any>
        >
      | undefined
  ) => Promise<FetchResult>,
  acceptedVulnIds: string[],
  findingId: string,
  values: {
    justification: string;
  }
): void => {
  if (isConfirmZeroRiskSelected) {
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void confirmZeroRisk({ //NOSONAR
      variables: {
        findingId,
        justification: values.justification,
        vulnerabilities: acceptedVulnIds,
      },
    });
  }
};

const isRejectZeroRiskSelectedHelper = (
  isRejectZeroRiskSelected: boolean,
  rejectZeroRisk: (
    options?:
      | MutationFunctionOptions<
          any,
          OperationVariables,
          DefaultContext,
          ApolloCache<any>
        >
      | undefined
  ) => Promise<FetchResult>,
  findingId: string,
  values: {
    justification: string;
  },
  rejectedVulnIds: string[]
): void => {
  if (isRejectZeroRiskSelected) {
    // Exception: FP(void operator is necessary)
    // eslint-disable-next-line
    void rejectZeroRisk({ //NOSONAR
      variables: {
        findingId,
        justification: values.justification,
        vulnerabilities: rejectedVulnIds,
      },
    });
  }
};

export {
  acceptationProps,
  confirmZeroRiskProps,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  onTreatmentChangeHelper,
  rejectZeroRiskProps,
};
