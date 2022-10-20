/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Formik } from "formik";
import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { HandleAcceptanceModalForm } from "./form";
import {
  acceptanceProps,
  confirmZeroRiskProps,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  rejectZeroRiskProps,
} from "./helpers";

import { Modal } from "components/Modal";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTANCE,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/queries";
import type {
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalProps,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/types";
import { authzPermissionsContext } from "utils/authz/config";

const HandleAcceptanceModal: React.FC<IHandleVulnerabilitiesAcceptanceModalProps> =
  ({
    findingId,
    groupName,
    vulns,
    handleCloseModal,
    refetchData,
  }: IHandleVulnerabilitiesAcceptanceModalProps): JSX.Element => {
    const { t } = useTranslation();
    const permissions: PureAbility<string> = useAbility(
      authzPermissionsContext
    );
    const canHandleVulnsAcceptance: boolean = permissions.can(
      "api_mutations_handle_vulnerabilities_acceptance_mutate"
    );
    const canConfirmZeroRiskVuln: boolean = permissions.can(
      "api_mutations_confirm_vulnerabilities_zero_risk_mutate"
    );

    const [acceptanceVulns, setAcceptanceVulns] = useState<IVulnDataAttr[]>([]);
    const [acceptedVulns, setAcceptedVulns] = useState<IVulnDataAttr[]>([]);
    const [rejectedVulns, setRejectedVulns] = useState<IVulnDataAttr[]>([]);
    const [hasAcceptedVulns, setHasAcceptedVulns] = useState<boolean>(false);
    const [hasRejectedVulns, setHasRejectedVulns] = useState<boolean>(false);

    const onAcceptanceVulnsChange: () => void = (): void => {
      const newAcceptedVulns: IVulnDataAttr[] = acceptanceVulns.reduce(
        (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
          vuln.acceptance === "APPROVED" ? [...acc, vuln] : acc,
        []
      );
      const newRejectedVulns: IVulnDataAttr[] = acceptanceVulns.reduce(
        (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
          vuln.acceptance === "REJECTED" ? [...acc, vuln] : acc,
        []
      );
      setAcceptedVulns(newAcceptedVulns);
      setRejectedVulns(newRejectedVulns);
      setHasAcceptedVulns(newAcceptedVulns.length !== 0);
      setHasRejectedVulns(newRejectedVulns.length !== 0);
    };
    useEffect(onAcceptanceVulnsChange, [acceptanceVulns]);

    // GraphQL operations
    const [handleAcceptance, { loading: handlingAcceptance }] = useMutation(
      HANDLE_VULNS_ACCEPTANCE,
      acceptanceProps(refetchData, handleCloseModal, findingId)
    );
    const [confirmZeroRisk, { loading: confirmingZeroRisk }] = useMutation(
      CONFIRM_VULNERABILITIES_ZERO_RISK,
      confirmZeroRiskProps(refetchData, handleCloseModal, groupName, findingId)
    );
    const [rejectZeroRisk, { loading: rejectingZeroRisk }] = useMutation(
      REJECT_VULNERABILITIES_ZERO_RISK,
      rejectZeroRiskProps(refetchData, handleCloseModal, groupName, findingId)
    );

    function getInitialTreatment(
      canHandleVulnsAccept: boolean,
      canConfirmZeroRisk: boolean
    ): string {
      if (canHandleVulnsAccept) {
        return "ACCEPTED_UNDEFINED";
      }

      return canConfirmZeroRisk ? "CONFIRM_REJECT_ZERO_RISK" : "";
    }

    function handleSubmit(values: IFormValues): void {
      const isAcceptedUndefinedSelected: boolean =
        values.treatment === "ACCEPTED_UNDEFINED";
      const isConfirmRejectZeroRiskSelected: boolean =
        values.treatment === "CONFIRM_REJECT_ZERO_RISK";

      const formValues = (({ justification }): { justification: string } => ({
        justification,
      }))(values);

      isAcceptedUndefinedSelectedHelper(
        isAcceptedUndefinedSelected,
        handleAcceptance,
        acceptedVulns,
        formValues,
        rejectedVulns
      );
      isConfirmZeroRiskSelectedHelper(
        isConfirmRejectZeroRiskSelected,
        confirmZeroRisk,
        acceptedVulns,
        formValues
      );
      isRejectZeroRiskSelectedHelper(
        isConfirmRejectZeroRiskSelected,
        rejectZeroRisk,
        formValues,
        rejectedVulns
      );
    }

    const initialTreatment: string = getInitialTreatment(
      canHandleVulnsAcceptance,
      canConfirmZeroRiskVuln
    );

    return (
      <React.StrictMode>
        <Modal
          open={true}
          title={t("searchFindings.tabDescription.handleAcceptanceModal.title")}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{
              justification: "",
              treatment: initialTreatment,
            }}
            name={"updateTreatmentAcceptance"}
            onSubmit={handleSubmit}
          >
            <HandleAcceptanceModalForm
              acceptanceVulnerabilities={acceptanceVulns}
              acceptedVulnerabilities={acceptedVulns}
              confirmingZeroRisk={confirmingZeroRisk}
              handleCloseModal={handleCloseModal}
              handlingAcceptance={handlingAcceptance}
              hasAcceptedVulns={hasAcceptedVulns}
              hasRejectedVulns={hasRejectedVulns}
              rejectedVulnerabilities={rejectedVulns}
              rejectingZeroRisk={rejectingZeroRisk}
              setAcceptanceVulns={setAcceptanceVulns}
              vulns={vulns}
            />
          </Formik>
        </Modal>
      </React.StrictMode>
    );
  };

export { HandleAcceptanceModal };
