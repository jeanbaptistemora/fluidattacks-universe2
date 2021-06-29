import type { FetchResult } from "@apollo/client";
import type { GraphQLError } from "graphql";
import { track } from "mixpanel-browser";

import type {
  IRequestVerificationVulnResult,
  IVerifyRequestVulnResult,
} from "./types";

import type { IVulnData } from ".";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleRequestVerification = (
  refetchData: () => void,
  clearSelected: () => void,
  setRequestState: () => void,
  data: IRequestVerificationVulnResult
): void => {
  if (data.requestVerificationVuln.success) {
    msgSuccess(
      translate.t("groupAlerts.requestedReattackSuccess"),
      translate.t("groupAlerts.updatedTitle")
    );
    refetchData();
    clearSelected();
    setRequestState();
  }
};

const handleRequestVerificationError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Request verification already requested":
        msgError(translate.t("groupAlerts.verificationAlreadyRequested"));
        break;
      case "Exception - The vulnerability has already been closed":
        msgError(translate.t("groupAlerts."));
        break;
      case "Exception - Vulnerability not found":
        msgError(translate.t("groupAlerts.noFound"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred requesting verification", error);
    }
  });
};

const handleVerifyRequest = (
  refetchData: () => void,
  clearSelected: () => void,
  setVerifyState: () => void,
  data: IVerifyRequestVulnResult,
  numberOfVulneabilities: number
): void => {
  if (data.verifyRequestVuln.success) {
    msgSuccess(
      translate.t(
        `groupAlerts.verifiedSuccess${
          numberOfVulneabilities > 1 ? "Plural" : ""
        }`
      ),
      translate.t("groupAlerts.updatedTitle")
    );
    refetchData();
    clearSelected();
    setVerifyState();
  }
};

const handleVerifyRequestError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    switch (error.message) {
      case "Exception - Error verification not requested":
        msgError(translate.t("groupAlerts.noVerificationRequested"));
        break;
      case "Exception - Vulnerability not found":
        msgError(translate.t("groupAlerts.noFound"));
        break;
      default:
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred verifying a request", error);
    }
  });
};

const handleSubmitHelper = (
  requestVerification: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  verifyRequest: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  findingId: string,
  values: { treatmentJustification: string },
  vulns: IVulnData[],
  vulnerabilitiesList: IVulnData[],
  isReattacking: boolean
): void => {
  if (isReattacking) {
    const vulnerabilitiesId: string[] = vulns.map(
      (vuln: IVulnData): string => vuln.id
    );

    track("RequestReattack");
    requestVerification({
      variables: {
        findingId,
        justification: values.treatmentJustification,
        vulnerabilities: vulnerabilitiesId,
      },
    }).catch((): undefined => undefined);
  } else {
    const openVulnsId: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnData): string[] =>
        vuln.currentState === "open" ? [...acc, vuln.id] : acc,
      []
    );
    const closedVulnsId: string[] = vulnerabilitiesList.reduce(
      (acc: string[], vuln: IVulnData): string[] =>
        vuln.currentState === "closed" ? [...acc, vuln.id] : acc,
      []
    );
    verifyRequest({
      variables: {
        closedVulns: closedVulnsId,
        findingId,
        justification: values.treatmentJustification,
        openVulns: openVulnsId,
      },
    }).catch((): undefined => undefined);
  }
};

export {
  handleRequestVerification,
  handleRequestVerificationError,
  handleVerifyRequest,
  handleVerifyRequestError,
  handleSubmitHelper,
};
