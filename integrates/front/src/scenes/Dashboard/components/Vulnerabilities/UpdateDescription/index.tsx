import type { FetchResult } from "@apollo/client";
import { Formik } from "formik";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
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

import type { IUpdateVulnerabilityForm, IVulnDataTypeAttr } from "../types";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IHistoricTreatment } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";

export const UpdateDescription: React.FC<IUpdateDescriptionProps> = ({
  changePermissions,
  findingId = "",
  isOpen = false,
  groupName,
  vulnerabilities,
  handleClearSelected,
  handleCloseModal,
  refetchData,
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
    isDescriptionPristine: boolean;
    isTreatmentDescriptionPristine: boolean;
    isTreatmentPristine: boolean;
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>;
    updateVulnerability: (
      dataTreatment: IUpdateVulnerabilityForm,
      isDescriptionPristine: boolean,
      isTreatmentDescriptionPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>;
  }>({
    isDescriptionPristine: true,
    isTreatmentDescriptionPristine: true,
    isTreatmentPristine: true,
    requestZeroRisk: async (): Promise<FetchResult<unknown>> =>
      Promise.resolve<FetchResult>({}),
    updateVulnerability: async (): Promise<void> => Promise.resolve(undefined),
  });
  const setConfigFn: (
    requestZeroRisk: (
      variables: Record<string, unknown>
    ) => Promise<FetchResult<unknown>>,
    updateVulnerability: (
      dataTreatment: IUpdateVulnerabilityForm,
      isDescriptionPristine: boolean,
      isTreatmentDescriptionPristine: boolean,
      isTreatmentPristine: boolean
    ) => Promise<void>,
    isDescriptionPristine: boolean,
    isTreatmentDescriptionPristine: boolean,
    isTreatmentPristine: boolean
  ) => void = useCallback(
    (
      requestZeroRisk: (
        variables: Record<string, unknown>
      ) => Promise<FetchResult<unknown>>,
      updateVulnerability: (
        dataTreatment: IUpdateVulnerabilityForm,
        isDescriptionPristine: boolean,
        isTreatmentDescriptionPristine: boolean,
        isTreatmentPristine: boolean
      ) => Promise<void>,
      isDescriptionPristine: boolean,
      isTreatmentDescriptionPristine: boolean,
      isTreatmentPristine: boolean
    ): void => {
      setFnConfig({
        isDescriptionPristine,
        isTreatmentDescriptionPristine,
        isTreatmentPristine,
        requestZeroRisk,
        updateVulnerability,
      });
    },
    []
  );

  useEffect((): void => {
    if (isOpen && changePermissions !== undefined) {
      changePermissions(groupName as string);
    }
  }, [groupName, isOpen, changePermissions]);

  return (
    <React.StrictMode>
      <ConfirmDialog
        message={t("searchFindings.tabDescription.approvalMessage")}
        title={t("searchFindings.tabDescription.approvalTitle")}
      >
        {(confirm): JSX.Element => {
          async function handleSubmit(
            values: IUpdateVulnerabilityForm
          ): Promise<void> {
            const changedToRequestZeroRisk: boolean =
              values.treatment === "REQUEST_ZERO_RISK";
            const changedToUndefined: boolean =
              values.treatment === "ACCEPTED_UNDEFINED" &&
              lastTreatment.treatment !== "ACCEPTED_UNDEFINED";

            await handleSubmitHelper(
              fnConfig.updateVulnerability,
              fnConfig.requestZeroRisk,
              confirm,
              values,
              findingId,
              vulnerabilities,
              changedToRequestZeroRisk,
              changedToUndefined,
              fnConfig.isDescriptionPristine,
              fnConfig.isTreatmentDescriptionPristine,
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
                severity:
                  Number(groupVulnLevel(vulnerabilities)) > 0
                    ? groupVulnLevel(vulnerabilities)
                    : "",
                source:
                  vulnerabilities.length === 1 &&
                  vulnerabilities[0].source.toUpperCase() !== "ASM"
                    ? vulnerabilities[0].source.toUpperCase()
                    : "",
                tag: _.join(_.intersection(...vulnsTags), ","),
                treatment: lastTreatment.treatment
                  .replace("NEW", "")
                  .replace("UNTREATED", ""),
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
                refetchData={refetchData}
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
