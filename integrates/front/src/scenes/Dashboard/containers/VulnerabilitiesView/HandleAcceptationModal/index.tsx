import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Formik } from "formik";
import React, { useEffect, useState } from "react";

import { HandleAcceptationModalForm } from "./form";
import {
  acceptationProps,
  confirmZeroRiskProps,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  rejectZeroRiskProps,
} from "./helpers";

import { Modal } from "components/Modal";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import type {
  IFormValues,
  IHandleVulnerabilitiesAcceptationModalProps,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { authzPermissionsContext } from "utils/authz/config";
import { translate } from "utils/translations/translate";

const HandleAcceptationModal: React.FC<IHandleVulnerabilitiesAcceptationModalProps> =
  (props: IHandleVulnerabilitiesAcceptationModalProps): JSX.Element => {
    const { findingId, groupName, vulns, handleCloseModal, refetchData } =
      props;

    const permissions: PureAbility<string> = useAbility(
      authzPermissionsContext
    );
    const canGetHistoricState: boolean = permissions.can(
      "api_resolvers_finding_historic_state_resolve"
    );
    const canRetrieveHacker: boolean = permissions.can(
      "api_resolvers_vulnerability_hacker_resolve"
    );
    const canRetrieveZeroRisk: boolean = permissions.can(
      "api_resolvers_finding_zero_risk_resolve"
    );
    const canHandleVulnsAcceptation: boolean = permissions.can(
      "api_mutations_handle_vulnerabilities_acceptation_mutate"
    );
    const canConfirmZeroRiskVuln: boolean = permissions.can(
      "api_mutations_confirm_vulnerabilities_zero_risk_mutate"
    );

    const [acceptationVulns, setAcceptationVulns] = useState<IVulnDataAttr[]>(
      []
    );
    const [acceptedVulns, setAcceptedVulns] = useState<IVulnDataAttr[]>([]);
    const [rejectedVulns, setRejectedVulns] = useState<IVulnDataAttr[]>([]);
    const [hasAcceptedVulns, setHasAcceptedVulns] = useState<boolean>(false);
    const [hasRejectedVulns, setHasRejectedVulns] = useState<boolean>(false);

    const onAcceptationVulnsChange: () => void = (): void => {
      const newAcceptedVulns: IVulnDataAttr[] = acceptationVulns.reduce(
        (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
          vuln.acceptation === "APPROVED" ? [...acc, vuln] : acc,
        []
      );
      const newRejectedVulns: IVulnDataAttr[] = acceptationVulns.reduce(
        (acc: IVulnDataAttr[], vuln: IVulnDataAttr): IVulnDataAttr[] =>
          vuln.acceptation === "REJECTED" ? [...acc, vuln] : acc,
        []
      );
      setAcceptedVulns(newAcceptedVulns);
      setRejectedVulns(newRejectedVulns);
      setHasAcceptedVulns(newAcceptedVulns.length !== 0);
      setHasRejectedVulns(newRejectedVulns.length !== 0);
    };
    useEffect(onAcceptationVulnsChange, [acceptationVulns]);

    // GraphQL operations
    const [handleAcceptation, { loading: handlingAcceptation }] = useMutation(
      HANDLE_VULNS_ACCEPTATION,
      acceptationProps(
        refetchData,
        handleCloseModal,
        canRetrieveHacker,
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
        canRetrieveHacker,
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
        canRetrieveHacker,
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

    function handleSubmit(values: IFormValues): void {
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
      isAcceptedUndefinedSelectedHelper(
        isAcceptedUndefinedSelected,
        handleAcceptation,
        acceptedVulnIds,
        findingId,
        formValues,
        rejectedVulnIds
      );
      isConfirmZeroRiskSelectedHelper(
        acceptedVulnIds.length !== 0,
        isConfirmRejectZeroRiskSelected,
        confirmZeroRisk,
        acceptedVulnIds,
        findingId,
        formValues
      );
      isRejectZeroRiskSelectedHelper(
        rejectedVulnIds.length !== 0,
        isConfirmRejectZeroRiskSelected,
        rejectZeroRisk,
        findingId,
        formValues,
        rejectedVulnIds
      );
    }

    const initialTreatment: string = getInitialTreatment(
      canHandleVulnsAcceptation,
      canConfirmZeroRiskVuln
    );

    return (
      <React.StrictMode>
        <Modal
          headerTitle={translate.t(
            "searchFindings.tabDescription.handleAcceptationModal.title"
          )}
          open={true}
          size={"extraLargeModal"}
        >
          <Formik
            enableReinitialize={true}
            initialValues={{
              justification: "",
              treatment: initialTreatment,
            }}
            name={"updateTreatmentAcceptation"}
            onSubmit={handleSubmit}
          >
            <HandleAcceptationModalForm
              acceptationVulns={acceptationVulns}
              acceptedVulns={acceptedVulns}
              confirmingZeroRisk={confirmingZeroRisk}
              handleCloseModal={handleCloseModal}
              handlingAcceptation={handlingAcceptation}
              hasAcceptedVulns={hasAcceptedVulns}
              hasRejectedVulns={hasRejectedVulns}
              rejectedVulns={rejectedVulns}
              rejectingZeroRisk={rejectingZeroRisk}
              setAcceptationVulns={setAcceptationVulns}
              vulns={vulns}
            />
          </Formik>
        </Modal>
      </React.StrictMode>
    );
  };

export { HandleAcceptationModal };
