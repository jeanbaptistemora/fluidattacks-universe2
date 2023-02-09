import type {
  ApolloError,
  FetchResult,
  InternalRefetchQueriesInclude,
  MutationFunctionOptions,
  MutationHookOptions,
} from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";

import { GET_FINDING_HEADER } from "../../queries";
import type { IVulnerabilitiesAttr } from "../types";
import {
  getRequestedZeroRiskVulns,
  getSubmittedVulns,
  getVulnsPendingOfAcceptance,
} from "../utils";
import type {
  IConfirmVulnZeroRiskResultAttr,
  IHandleVulnerabilitiesAcceptanceResultAttr,
  IRejectZeroRiskVulnResultAttr,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";
import { GET_FINDING_AND_GROUP_INFO } from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/queries";
import { GET_GROUP_VULNERABILITIES } from "scenes/Dashboard/containers/Group-Content/GroupFindingsView/queries";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const onTreatmentChangeHelper = (
  isAcceptedUndefinedSelected: boolean,
  vulns: IVulnerabilitiesAttr[],
  setAcceptanceVulns: (pendingVulnsToHandleAcceptance: IVulnDataAttr[]) => void,
  isConfirmRejectZeroRiskSelected: boolean,
  isConfirmRejectVulnerabilitySelected: boolean
): void => {
  if (isAcceptedUndefinedSelected) {
    const pendingVulnsToHandleAcceptance: IVulnDataAttr[] =
      getVulnsPendingOfAcceptance(vulns);
    setAcceptanceVulns(pendingVulnsToHandleAcceptance);
  } else if (isConfirmRejectZeroRiskSelected) {
    const requestedZeroRiskVulns: IVulnDataAttr[] =
      getRequestedZeroRiskVulns(vulns);
    setAcceptanceVulns([...requestedZeroRiskVulns]);
  } else if (isConfirmRejectVulnerabilitySelected) {
    const submittedVulns: IVulnDataAttr[] = getSubmittedVulns(vulns);
    setAcceptanceVulns([...submittedVulns]);
  } else {
    setAcceptanceVulns([]);
  }
};

const acceptanceProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId?: string
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
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_AND_GROUP_INFO,
              variables: {
                findingId,
              },
            },
          ],
  };
};

const confirmVulnerabilityHelper = (
  isConfirmRejectVulnerabilitySelected: boolean,
  confirmVulnerabilities: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  confirmedVulns: IVulnDataAttr[],
  values: {
    justification: string;
  }
): void => {
  if (isConfirmRejectVulnerabilitySelected && !_.isEmpty(confirmedVulns)) {
    Object.entries(
      _.groupBy(
        confirmedVulns,
        (vulnerability: IVulnDataAttr): string => vulnerability.findingId
      )
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const confirmedVulnIds: string[] = chunkedVulnerabilities.map(
          (vulnerability: IVulnDataAttr): string => vulnerability.id
        );
        await confirmVulnerabilities({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: confirmedVulnIds,
          },
        });
      }
    );
  }
};

const confirmZeroRiskProps = (
  refetchData: () => void,
  handleCloseModal: () => void,
  findingId?: string
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
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_AND_GROUP_INFO,
              variables: {
                findingId,
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
  groupName: string,
  findingId?: string
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
    refetchQueries: (): InternalRefetchQueriesInclude =>
      findingId === undefined
        ? []
        : [
            {
              query: GET_FINDING_AND_GROUP_INFO,
              variables: {
                findingId,
              },
            },
            {
              query: GET_FINDING_HEADER,
              variables: {
                findingId,
              },
            },
            {
              query: GET_GROUP_VULNERABILITIES,
              variables: {
                first: 1200,
                groupName,
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
  acceptedVulns: IVulnDataAttr[],
  values: {
    justification: string;
  },
  rejectedVulns: IVulnDataAttr[]
): void => {
  if (isAcceptedUndefinedSelected) {
    const chunksize = 10;
    if (!_.isEmpty(acceptedVulns)) {
      Object.entries(
        _.groupBy(
          acceptedVulns,
          (vuln: IVulnDataAttr): string => vuln.findingId
        )
      ).forEach(
        ([findingId, chunkedVulnerabilities]: [
          string,
          IVulnDataAttr[]
        ]): void => {
          const acceptedVulnIds: string[] = chunkedVulnerabilities.map(
            (vuln: IVulnDataAttr): string => vuln.id
          );
          const acceptedChunks = _.chunk(acceptedVulnIds, chunksize);
          acceptedChunks.map(async (acceptVulns): Promise<void> => {
            await handleAcceptance({
              variables: {
                acceptedVulnerabilities: acceptVulns,
                findingId,
                justification: values.justification,
                rejectedVulnerabilities: [],
              },
            });
          });
        }
      );
    }
    if (!_.isEmpty(rejectedVulns)) {
      Object.entries(
        _.groupBy(
          rejectedVulns,
          (vuln: IVulnDataAttr): string => vuln.findingId
        )
      ).forEach(
        ([findingId, chunkedVulnerabilities]: [
          string,
          IVulnDataAttr[]
        ]): void => {
          const rejectedVulnIds: string[] = chunkedVulnerabilities.map(
            (vuln: IVulnDataAttr): string => vuln.id
          );
          const rejectedChunks = _.chunk(rejectedVulnIds, chunksize);
          rejectedChunks.map(async (rejectVulns): Promise<void> => {
            await handleAcceptance({
              variables: {
                acceptedVulnerabilities: [],
                findingId,
                justification: values.justification,
                rejectedVulnerabilities: rejectVulns,
              },
            });
          });
        }
      );
    }
  }
};

const isConfirmZeroRiskSelectedHelper = (
  isConfirmZeroRiskSelected: boolean,
  confirmZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  acceptedVulns: IVulnDataAttr[],
  values: {
    justification: string;
  }
): void => {
  if (isConfirmZeroRiskSelected && !_.isEmpty(acceptedVulns)) {
    Object.entries(
      _.groupBy(acceptedVulns, (vuln: IVulnDataAttr): string => vuln.findingId)
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const acceptedVulnIds: string[] = chunkedVulnerabilities.map(
          (vuln: IVulnDataAttr): string => vuln.id
        );
        await confirmZeroRisk({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: acceptedVulnIds,
          },
        });
      }
    );
  }
};

const isRejectZeroRiskSelectedHelper = (
  isRejectZeroRiskSelected: boolean,
  rejectZeroRisk: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  values: {
    justification: string;
  },
  rejectedVulns: IVulnDataAttr[]
): void => {
  if (isRejectZeroRiskSelected && !_.isEmpty(rejectedVulns)) {
    Object.entries(
      _.groupBy(rejectedVulns, (vuln: IVulnDataAttr): string => vuln.findingId)
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const rejectedVulnIds: string[] = chunkedVulnerabilities.map(
          (vuln: IVulnDataAttr): string => vuln.id
        );
        await rejectZeroRisk({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: rejectedVulnIds,
          },
        });
      }
    );
  }
};

const rejectVulnerabilityHelper = (
  isConfirmRejectVulnerabilitySelected: boolean,
  rejectVulnerabilities: (
    options?: MutationFunctionOptions | undefined
  ) => Promise<FetchResult>,
  values: {
    justification: string;
  },
  rejectedVulns: IVulnDataAttr[]
): void => {
  if (isConfirmRejectVulnerabilitySelected && !_.isEmpty(rejectedVulns)) {
    Object.entries(
      _.groupBy(
        rejectedVulns,
        (vulnerability: IVulnDataAttr): string => vulnerability.findingId
      )
    ).forEach(
      async ([findingId, chunkedVulnerabilities]: [
        string,
        IVulnDataAttr[]
      ]): Promise<void> => {
        const rejectedVulnIds: string[] = chunkedVulnerabilities.map(
          (vulnerability: IVulnDataAttr): string => vulnerability.id
        );
        await rejectVulnerabilities({
          variables: {
            findingId,
            justification: values.justification,
            vulnerabilities: rejectedVulnIds,
          },
        });
      }
    );
  }
};

export {
  acceptanceProps,
  confirmZeroRiskProps,
  confirmVulnerabilityHelper,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  onTreatmentChangeHelper,
  rejectVulnerabilityHelper,
  rejectZeroRiskProps,
};
