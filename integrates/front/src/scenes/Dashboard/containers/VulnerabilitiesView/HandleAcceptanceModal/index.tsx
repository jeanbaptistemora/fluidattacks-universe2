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
    const canGetHistoricState: boolean = permissions.can(
      "api_resolvers_finding_historic_state_resolve"
    );
    const canRetrieveZeroRisk: boolean = permissions.can(
      "api_resolvers_finding_zero_risk_connection_resolve"
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
      acceptanceProps(
        refetchData,
        handleCloseModal,
        canRetrieveZeroRisk,
        findingId,
        groupName
      )
    );
    const [confirmZeroRisk, { loading: confirmingZeroRisk }] = useMutation(
      CONFIRM_VULNERABILITIES_ZERO_RISK,
      confirmZeroRiskProps(
        refetchData,
        handleCloseModal,
        canRetrieveZeroRisk,
        findingId,
        groupName,
        canGetHistoricState
      )
    );
    const [rejectZeroRisk, { loading: rejectingZeroRisk }] = useMutation(
      REJECT_VULNERABILITIES_ZERO_RISK,
      rejectZeroRiskProps(
        refetchData,
        handleCloseModal,
        canRetrieveZeroRisk,
        findingId,
        groupName,
        canGetHistoricState
      )
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

    async function handleSubmit(values: IFormValues): Promise<void> {
      const isAcceptedUndefinedSelected: boolean =
        values.treatment === "ACCEPTED_UNDEFINED";
      const isConfirmRejectZeroRiskSelected: boolean =
        values.treatment === "CONFIRM_REJECT_ZERO_RISK";

      const formValues = (({ justification }): { justification: string } => ({
        justification,
      }))(values);

      const acceptedVulnIds: string[] = acceptedVulns.map(
        (vuln: IVulnDataAttr): string => vuln.id
      );
      const rejectedVulnIds: string[] = rejectedVulns.map(
        (vuln: IVulnDataAttr): string => vuln.id
      );
      await isAcceptedUndefinedSelectedHelper(
        isAcceptedUndefinedSelected,
        handleAcceptance,
        acceptedVulnIds,
        findingId,
        formValues,
        rejectedVulnIds
      );
      await isConfirmZeroRiskSelectedHelper(
        acceptedVulnIds.length !== 0,
        isConfirmRejectZeroRiskSelected,
        confirmZeroRisk,
        acceptedVulnIds,
        findingId,
        formValues
      );
      await isRejectZeroRiskSelectedHelper(
        rejectedVulnIds.length !== 0,
        isConfirmRejectZeroRiskSelected,
        rejectZeroRisk,
        findingId,
        formValues,
        rejectedVulnIds
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
