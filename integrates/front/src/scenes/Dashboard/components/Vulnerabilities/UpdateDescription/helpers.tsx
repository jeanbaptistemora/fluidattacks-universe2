import type { FetchResult } from "@apollo/client";
import type { ExecutionResult, GraphQLError } from "graphql";
import _ from "lodash";
import { track } from "mixpanel-browser";
import React from "react";

import type {
  IRemoveTagResultAttr,
  IRequestVulnZeroRiskResultAttr,
  IUpdateVulnDescriptionResultAttr,
} from "./types";
import { groupLastHistoricTreatment } from "./utils";

import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
} from "../types";
import type { IConfirmFn } from "components/ConfirmDialog";
import { Alert } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const isTheFormPristine = (
  isTreatmentValuesPristine: boolean,
  formValues: IUpdateTreatmentVulnerabilityForm,
  vulnerabilities: IVulnDataTypeAttr[]
): boolean => {
  return (
    isTreatmentValuesPristine &&
    (_.isEmpty(formValues.justification) ||
      (groupLastHistoricTreatment(vulnerabilities).justification as string) ===
        formValues.justification)
  );
};

const deleteTagVulnHelper = (result: IRemoveTagResultAttr): void => {
  if (!_.isUndefined(result)) {
    if (result.removeTags.success) {
      msgSuccess(
        translate.t("searchFindings.tabDescription.updateVulnerabilities"),
        translate.t("groupAlerts.titleSuccess")
      );
    }
  }
};

type VulnUpdateResult = ExecutionResult<IUpdateVulnDescriptionResultAttr>;

const getResults = async (
  updateVuln: (variables: Record<string, unknown>) => Promise<VulnUpdateResult>,
  vulnerabilities: IVulnDataTypeAttr[],
  dataTreatment: IUpdateTreatmentVulnerabilityForm,
  findingId: string,
  isEditPristine: boolean,
  isTreatmentPristine: boolean
): Promise<VulnUpdateResult[]> => {
  const chunkSize = 10;
  const vulnChunks = _.chunk(vulnerabilities, chunkSize);
  const updateChunks = vulnChunks.map(
    (chunk): (() => Promise<VulnUpdateResult[]>) =>
      async (): Promise<VulnUpdateResult[]> => {
        const updates = chunk.map(
          async (vuln): Promise<VulnUpdateResult> =>
            updateVuln({
              variables: {
                acceptanceDate: dataTreatment.acceptanceDate,
                externalBugTrackingSystem:
                  dataTreatment.externalBugTrackingSystem,
                findingId,
                isVulnInfoChanged: !isEditPristine,
                isVulnTreatmentChanged: !isTreatmentPristine,
                justification: dataTreatment.justification,
                severity: _.isEmpty(String(dataTreatment.severity))
                  ? -1
                  : Number(dataTreatment.severity),
                tag: dataTreatment.tag,
                treatment: isTreatmentPristine
                  ? "IN_PROGRESS"
                  : dataTreatment.treatment,
                treatmentManager: _.isEmpty(dataTreatment.treatmentManager)
                  ? undefined
                  : dataTreatment.treatmentManager,
                vulnerabilityId: vuln.id,
              },
            })
        );

        return Promise.all(updates);
      }
  );

  // Sequentially execute chunks
  return updateChunks.reduce(
    async (previousValue, currentValue): Promise<VulnUpdateResult[]> => [
      ...(await previousValue),
      ...(await currentValue()),
    ],
    Promise.resolve<VulnUpdateResult[]>([])
  );
};

const getAreAllMutationValid = (
  results: ExecutionResult<IUpdateVulnDescriptionResultAttr>[]
): boolean[] => {
  return results.map(
    (result: ExecutionResult<IUpdateVulnDescriptionResultAttr>): boolean => {
      if (!_.isUndefined(result.data) && !_.isNull(result.data)) {
        const updateInfoSuccess: boolean = _.isUndefined(
          result.data.updateVulnerabilityTreatment
        )
          ? true
          : result.data.updateVulnerabilityTreatment.success;
        const updateTreatmentSuccess: boolean = _.isUndefined(
          result.data.updateVulnerabilitiesTreatment
        )
          ? true
          : result.data.updateVulnerabilitiesTreatment.success;

        return updateInfoSuccess && updateTreatmentSuccess;
      }

      return false;
    }
  );
};

const dataTreatmentTrackHelper = (
  dataTreatment: IUpdateTreatmentVulnerabilityForm
): void => {
  if (dataTreatment.tag !== undefined) {
    track("AddVulnerabilityTag");
  }
  if (dataTreatment.severity !== undefined) {
    track("AddVulnerabilityLevel");
  }
};

const validMutationsHelper = (
  handleCloseModal: () => void,
  areAllMutationValid: boolean[],
  vulnerabilities: IVulnDataTypeAttr[]
): void => {
  if (areAllMutationValid.every(Boolean)) {
    track("UpdatedTreatmentVulnerabilities", {
      batchSize: vulnerabilities.length,
    });
    msgSuccess(
      translate.t("searchFindings.tabDescription.updateVulnerabilities"),
      translate.t("groupAlerts.titleSuccess")
    );
    handleCloseModal();
  }
};

const handleUpdateVulnTreatmentError = (updateError: unknown): void => {
  if (_.includes(String(updateError), "Invalid treatment manager")) {
    msgError(translate.t("groupAlerts.invalidTreatmentMgr"));
  } else if (
    _.includes(
      String(updateError),
      translate.t("searchFindings.tabVuln.alerts.maximumNumberOfAcceptances")
    )
  ) {
    msgError(
      translate.t("searchFindings.tabVuln.alerts.maximumNumberOfAcceptances")
    );
  } else if (
    _.includes(
      String(updateError),
      translate.t("groupAlerts.organizationPolicies.exceedsAcceptanceDate")
    )
  ) {
    msgError(
      translate.t("groupAlerts.organizationPolicies.exceedsAcceptanceDate")
    );
  } else if (
    _.includes(
      String(updateError),
      translate.t("searchFindings.tabVuln.exceptions.severityOutOfRange")
    )
  ) {
    msgError(
      translate.t("groupAlerts.organizationPolicies.severityOutOfRange")
    );
  } else if (
    _.includes(
      String(updateError),
      translate.t("searchFindings.tabVuln.exceptions.sameValues")
    )
  ) {
    msgError(translate.t("searchFindings.tabVuln.exceptions.sameValues"));
  } else {
    msgError(translate.t("groupAlerts.errorTextsad"));
    Logger.warning("An error occurred updating vuln treatment", updateError);
  }
};

const requestZeroRiskHelper = (
  handleClearSelected: () => void,
  handleCloseModal: () => void,
  requestZeroRiskVulnResult: IRequestVulnZeroRiskResultAttr
): void => {
  if (requestZeroRiskVulnResult.requestVulnerabilitiesZeroRisk.success) {
    msgSuccess(
      translate.t("groupAlerts.requestedZeroRiskSuccess"),
      translate.t("groupAlerts.updatedTitle")
    );
    handleClearSelected();
    handleCloseModal();
  }
};

const handleRequestZeroRiskError = (
  graphQLErrors: readonly GraphQLError[]
): void => {
  graphQLErrors.forEach((error: GraphQLError): void => {
    if (
      error.message ===
      "Exception - Zero risk vulnerability is already requested"
    ) {
      msgError(translate.t("groupAlerts.zeroRiskAlreadyRequested"));
    } else if (
      error.message ===
      "Exception - Justification must have a maximum of 5000 characters"
    ) {
      msgError(translate.t("validations.invalidFieldLength"));
    } else {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred requesting zero risk vuln", error);
    }
  });
};

const handleSubmitHelper = async (
  handleUpdateVulnTreatment: (
    dataTreatment: IUpdateTreatmentVulnerabilityForm,
    isEditPristine: boolean,
    isTreatmentPristine: boolean
  ) => Promise<void>,
  requestZeroRisk: (
    variables: Record<string, unknown>
  ) => Promise<FetchResult<unknown>>,
  confirm: IConfirmFn,
  values: IUpdateTreatmentVulnerabilityForm,
  findingId: string,
  vulnerabilities: IVulnDataTypeAttr[],
  changedToRequestZeroRisk: boolean,
  changedToUndefined: boolean,
  isEditPristine: boolean,
  isTreatmentPristine: boolean
  // Exception: FP(parameters are necessary)
  // eslint-disable-next-line
): Promise<void> => { // NOSONAR
  if (changedToRequestZeroRisk) {
    await requestZeroRisk({
      variables: {
        findingId,
        justification: values.justification,
        vulnerabilities: vulnerabilities.map(
          (vuln: IVulnDataTypeAttr): string => vuln.id
        ),
      },
    });
  } else if (changedToUndefined) {
    confirm((): void => {
      // Exception: FP(void operator is necessary)
      // eslint-disable-next-line
      void handleUpdateVulnTreatment(values, isEditPristine, isTreatmentPristine); //NOSONAR
    });
  } else {
    await handleUpdateVulnTreatment(
      values,
      isEditPristine,
      isTreatmentPristine
    );
  }
};

const tagReminderAlert = (isTreatmentPristine: boolean): JSX.Element => {
  return isTreatmentPristine ? (
    <div />
  ) : (
    <Alert>
      {"*"}&nbsp;
      {translate.t("searchFindings.tabVuln.alerts.tagReminder")}
    </Alert>
  );
};

const treatmentChangeAlert = (isTreatmentPristine: boolean): JSX.Element => {
  return isTreatmentPristine ? (
    <div />
  ) : (
    <Alert>
      {"*"}&nbsp;
      {translate.t("searchFindings.tabVuln.alerts.treatmentChange")}
    </Alert>
  );
};

const hasNewVulnsAlert = (
  vulnerabilities: IVulnDataTypeAttr[],
  hasNewVulns: boolean,
  isAcceptedSelected: boolean,
  isAcceptedUndefinedSelected: boolean,
  isInProgressSelected: boolean
): JSX.Element => {
  return hasNewVulns &&
    !(
      isAcceptedSelected ||
      isAcceptedUndefinedSelected ||
      isInProgressSelected
    ) ? (
    <Alert>
      {"*"}&nbsp;
      {translate.t("searchFindings.tabVuln.alerts.hasNewVulns", {
        count: vulnerabilities.length,
      })}
    </Alert>
  ) : (
    <div />
  );
};

export {
  isTheFormPristine,
  deleteTagVulnHelper,
  getResults,
  getAreAllMutationValid,
  dataTreatmentTrackHelper,
  validMutationsHelper,
  handleUpdateVulnTreatmentError,
  requestZeroRiskHelper,
  handleRequestZeroRiskError,
  handleSubmitHelper,
  tagReminderAlert,
  treatmentChangeAlert,
  hasNewVulnsAlert,
};
