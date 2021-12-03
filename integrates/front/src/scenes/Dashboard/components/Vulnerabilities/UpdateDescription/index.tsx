import type { FetchResult } from "@apollo/client";
import { Formik } from "formik";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { UpdateTreatmentModal } from "./form";
import { handleSubmitHelper } from "./helpers";
import type { IUpdateDescriptionProps } from "./types";
import {
  groupExternalBugTrackingSystem,
  groupLastHistoricTreatment,
  groupVulnLevel,
  sortTags,
} from "./utils";

import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnDataTypeAttr,
} from "../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/DescriptionView/types";

export const UpdateDescription: React.FC<IUpdateDescriptionProps> = ({
  findingId,
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
}: IUpdateDescriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const lastTreatment: IHistoricTreatment = {
    ...groupLastHistoricTreatment(vulnerabilities),
    justification: "",
  };
  const vulnsTags: string[][] = vulnerabilities.map(
    (vuln: IVulnDataTypeAttr): string[] => sortTags(vuln.tag)
  );

  const [fnConfig, setFnConfig] = useState<{
    isEditPristine: boolean;
    isTreatmentPristine: boolean;
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>;
    updateDescription: (
      dataTreatment: IUpdateTreatmentVulnerabilityForm,
      isEditPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>;
  }>({
    isEditPristine: true,
    isTreatmentPristine: true,
    requestZeroRisk: async (): Promise<FetchResult<unknown>> =>
      Promise.resolve<FetchResult>({}),
    updateDescription: async (): Promise<void> => Promise.resolve(undefined),
  });
  const setConfigFn: (
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>,
    updateDescription: (
      dataTreatment: IUpdateTreatmentVulnerabilityForm,
      isEditPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>,
    isEditPristine: boolean,
    isTreatmentPristine: boolean
  ) => void = useCallback(
    (
      requestZeroRisk: (
        variables: Record<string, unknown>
      ) => Promise<FetchResult<unknown>>,
      updateDescription: (
        dataTreatment: IUpdateTreatmentVulnerabilityForm,
        isEditPristine: boolean,
        isTreatmentPristine: boolean
      ) => Promise<void>,
      isEditPristine: boolean,
      isTreatmentPristine: boolean
    ): void => {
      setFnConfig({
        isEditPristine,
        isTreatmentPristine,
        requestZeroRisk,
        updateDescription,
      });
    },
    []
  );

  return (
    <React.StrictMode>
      <ConfirmDialog
        message={t("searchFindings.tabDescription.approvalMessage")}
        title={t("searchFindings.tabDescription.approvalTitle")}
      >
        {(confirm: IConfirmFn): JSX.Element => {
          async function handleSubmit(
            values: IUpdateTreatmentVulnerabilityForm
          ): Promise<void> {
            const changedToRequestZeroRisk: boolean =
              values.treatment === "REQUEST_ZERO_RISK";
            const changedToUndefined: boolean =
              values.treatment === "ACCEPTED_UNDEFINED" &&
              lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

            await handleSubmitHelper(
              fnConfig.updateDescription,
              fnConfig.requestZeroRisk,
              confirm,
              values,
              findingId,
              vulnerabilities,
              changedToRequestZeroRisk,
              changedToUndefined,
              fnConfig.isEditPristine,
              fnConfig.isTreatmentPristine
            );
          }

          return (
            <Formik
              enableReinitialize={true}
              initialValues={{
                acceptanceDate: lastTreatment.acceptanceDate,
                acceptanceStatus: lastTreatment.acceptanceStatus,
                assigned: lastTreatment.assigned,
                date: lastTreatment.date,
                externalBugTrackingSystem:
                  groupExternalBugTrackingSystem(vulnerabilities),
                justification: lastTreatment.justification,
                severity: groupVulnLevel(vulnerabilities),
                tag: _.join(_.intersection(...vulnsTags), ","),
                treatment: lastTreatment.treatment.replace("NEW", ""),
                user: lastTreatment.user,
              }}
              name={"editTreatmentVulnerability"}
              onSubmit={handleSubmit}
            >
              <UpdateTreatmentModal
                findingId={findingId}
                groupName={groupName}
                handleClearSelected={handleClearSelected}
                handleCloseModal={handleCloseModal}
                setConfigFn={setConfigFn}
                vulnerabilities={vulnerabilities}
              />
            </Formik>
          );
        }}
      </ConfirmDialog>
    </React.StrictMode>
  );
};
