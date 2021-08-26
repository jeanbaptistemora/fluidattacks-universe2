import _ from "lodash";
import { track } from "mixpanel-browser";

import type { IVulnData } from ".";
import type {
  IRequestVulnVerificationResult,
  IVerifyRequestVulnResult,
  ReattackVulnerabilitiesResult,
  VerifyVulnerabilitiesResult,
} from "scenes/Dashboard/components/UpdateVerificationModal/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const handleRequestVerification = (
  clearSelected: () => void,
  setRequestState: () => void,
  data: boolean
): void => {
  if (data) {
    msgSuccess(
      translate.t("groupAlerts.requestedReattackSuccess"),
      translate.t("groupAlerts.updatedTitle")
    );
    clearSelected();
    setRequestState();
  }
};

const handleRequestVerificationError = (error: unknown): void => {
  switch (String(error)) {
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
};

const handleVerifyRequest = (
  clearSelected: () => void,
  setVerifyState: () => void,
  data: boolean,
  numberOfVulneabilities: number
): void => {
  if (data) {
    msgSuccess(
      translate.t(
        `groupAlerts.verifiedSuccess${
          numberOfVulneabilities > 1 ? "Plural" : ""
        }`
      ),
      translate.t("groupAlerts.updatedTitle")
    );
    clearSelected();
    setVerifyState();
  }
};

const handleVerifyRequestError = (error: unknown): void => {
  switch (String(error)) {
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
};

const getAreAllMutationValid = (
  results: ReattackVulnerabilitiesResult[] | VerifyVulnerabilitiesResult[]
): boolean[] => {
  return results.map(
    (
      result: ReattackVulnerabilitiesResult | VerifyVulnerabilitiesResult
    ): boolean => {
      if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
        const reattackSuccess: boolean = _.isUndefined(
          (result.data as IRequestVulnVerificationResult)
            .requestVulnerabilitiesVerification
        )
          ? false
          : (result.data as IRequestVulnVerificationResult)
              .requestVulnerabilitiesVerification.success;

        const verifySuccess: boolean = _.isUndefined(
          (result.data as IVerifyRequestVulnResult).verifyVulnerabilitiesRequest
        )
          ? false
          : (result.data as IVerifyRequestVulnResult)
              .verifyVulnerabilitiesRequest.success;

        return reattackSuccess || verifySuccess;
      }

      return false;
    }
  );
};

const handleSubmitHelper = async (
  requestVerification: (
    variables: Record<string, unknown>
  ) => Promise<ReattackVulnerabilitiesResult>,
  verifyRequest: (
    variables: Record<string, unknown>
  ) => Promise<VerifyVulnerabilitiesResult>,
  findingId: string,
  values: { treatmentJustification: string },
  vulns: IVulnData[],
  vulnerabilitiesList: IVulnData[],
  isReattacking: boolean
): Promise<ReattackVulnerabilitiesResult[] | VerifyVulnerabilitiesResult[]> => {
  const chunkSize = 100;
  if (isReattacking) {
    const vulnerabilitiesId: string[] = vulns.map(
      (vuln: IVulnData): string => vuln.id
    );

    track("RequestReattack");
    const vulnerabilitiesIdsChunks: string[][] = _.chunk(
      vulnerabilitiesId,
      chunkSize
    );
    const requestedChunks = vulnerabilitiesIdsChunks.map(
      (
          chunkedVulnerabilitiesIds
        ): (() => Promise<ReattackVulnerabilitiesResult[]>) =>
        async (): Promise<ReattackVulnerabilitiesResult[]> => {
          return Promise.all([
            requestVerification({
              variables: {
                findingId,
                justification: values.treatmentJustification,
                vulnerabilities: chunkedVulnerabilitiesIds,
              },
            }),
          ]);
        }
    );

    return requestedChunks.reduce(
      async (
        previousValue,
        currentValue
      ): Promise<ReattackVulnerabilitiesResult[]> => [
        ...(await previousValue),
        ...(await currentValue()),
      ],
      Promise.resolve<ReattackVulnerabilitiesResult[]>([])
    );
  }
  const VulnerabilitiesListChunks: IVulnData[][] = _.chunk(
    vulnerabilitiesList,
    chunkSize
  );
  const verifiedChunks = VulnerabilitiesListChunks.map(
    (
        chunkedVulnerabilitiesList
      ): (() => Promise<VerifyVulnerabilitiesResult[]>) =>
      async (): Promise<VerifyVulnerabilitiesResult[]> => {
        const openVulnsId: string[] = chunkedVulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.currentState === "open" ? [...acc, vuln.id] : acc,
          []
        );
        const closedVulnsId: string[] = chunkedVulnerabilitiesList.reduce(
          (acc: string[], vuln: IVulnData): string[] =>
            vuln.currentState === "closed" ? [...acc, vuln.id] : acc,
          []
        );

        return Promise.all([
          verifyRequest({
            variables: {
              closedVulns: closedVulnsId,
              findingId,
              justification: values.treatmentJustification,
              openVulns: openVulnsId,
            },
          }),
        ]);
      }
  );

  return verifiedChunks.reduce(
    async (
      previousValue,
      currentValue
    ): Promise<VerifyVulnerabilitiesResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VerifyVulnerabilitiesResult[]>([])
  );
};

export {
  getAreAllMutationValid,
  handleRequestVerification,
  handleRequestVerificationError,
  handleVerifyRequest,
  handleVerifyRequestError,
  handleSubmitHelper,
};
