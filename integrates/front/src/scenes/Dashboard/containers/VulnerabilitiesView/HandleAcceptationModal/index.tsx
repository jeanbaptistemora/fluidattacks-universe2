import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import _ from "lodash";
import React, { useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { Dispatch } from "redux";
import { formValueSelector, submit } from "redux-form";

import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import {
  acceptationProps,
  confirmZeroRiskProps,
  isAcceptedUndefinedSelectedHelper,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  onTreatmentChangeHelper,
  rejectZeroRiskProps,
} from "./helpers";
import { JustificationField } from "./JustificationField";
import { TreatmentField } from "./TreatmentField";
import { ZeroRiskTable } from "./ZeroRiskTable";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  HANDLE_VULNS_ACCEPTATION,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/queries";
import type {
  IHandleVulnerabilitiesAcceptationModalProps,
  IVulnDataAttr,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptationModal/types";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
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
    const canRetrieveAnalyst: boolean = permissions.can(
      "api_resolvers_vulnerability_analyst_resolve"
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

    const dispatch: Dispatch = useDispatch();

    const [acceptationVulns, setAcceptationVulns] = useState<IVulnDataAttr[]>(
      []
    );
    const [acceptedVulns, setAcceptedVulns] = useState<IVulnDataAttr[]>([]);
    const [rejectedVulns, setRejectedVulns] = useState<IVulnDataAttr[]>([]);
    const [hasAcceptedVulns, setHasAcceptedVulns] = useState<boolean>(false);
    const [hasRejectedVulns, setHasRejectedVulns] = useState<boolean>(false);

    const formValues: Dictionary<string> = useSelector(
      (state: Record<string, unknown>): Dictionary<string> =>
        // It is necessary since formValueSelector returns an any type
        // eslint-disable-next-line @typescript-eslint/no-unsafe-return
        formValueSelector("updateTreatmentAcceptation")(state, "treatment", "")
    );

    const isAcceptedUndefinedSelected: boolean =
      formValues.treatment === "ACCEPTED_UNDEFINED";
    const isConfirmRejectZeroRiskSelected: boolean =
      formValues.treatment === "CONFIRM_REJECT_ZERO_RISK";

    // Side effects
    const onTreatmentChange: () => void = (): void => {
      onTreatmentChangeHelper(
        isAcceptedUndefinedSelected,
        vulns,
        setAcceptationVulns,
        isConfirmRejectZeroRiskSelected
      );
    };
    useEffect(onTreatmentChange, [
      isAcceptedUndefinedSelected,
      isConfirmRejectZeroRiskSelected,
      vulns,
    ]);

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
        canRetrieveAnalyst,
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
        canRetrieveAnalyst,
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
        canRetrieveAnalyst,
        canRetrieveZeroRisk,
        findingId,
        groupName,
        canGetHistoricState
      )
    );

    function handleUpdateTreatmentAcceptation(): void {
      dispatch(submit("updateTreatmentAcceptation"));
    }

    function getInitialTreatment(
      canHandleVulnsAccept: boolean,
      canConfirmZeroRisk: boolean
    ): string {
      if (canHandleVulnsAccept) {
        return "ACCEPTED_UNDEFINED";
      }

      return canConfirmZeroRisk ? "CONFIRM_REJECT_ZERO_RISK" : "";
    }

    function handleSubmit(values: { justification: string }): void {
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
        values,
        rejectedVulnIds
      );
      isConfirmZeroRiskSelectedHelper(
        acceptedVulnIds.length !== 0,
        confirmZeroRisk,
        acceptedVulnIds,
        findingId,
        values
      );
      isRejectZeroRiskSelectedHelper(
        rejectedVulnIds.length !== 0,
        rejectZeroRisk,
        findingId,
        values,
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
        >
          <GenericForm
            initialValues={{
              treatment: _.isEmpty(formValues.treatment)
                ? initialTreatment
                : formValues.treatment,
            }}
            name={"updateTreatmentAcceptation"}
            onSubmit={handleSubmit}
          >
            <Row>
              <Col50>
                <TreatmentField />
              </Col50>
            </Row>
            <Row>
              <Col100>
                <AcceptedUndefinedTable
                  acceptationVulns={acceptationVulns}
                  isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
                  setAcceptationVulns={setAcceptationVulns}
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <ZeroRiskTable
                  acceptationVulns={acceptationVulns}
                  setAcceptationVulns={setAcceptationVulns}
                />
              </Col100>
            </Row>
            <Row>
              <Col100>
                <JustificationField
                  isConfirmZeroRiskSelected={acceptedVulns.length !== 0}
                  isRejectZeroRiskSelected={rejectedVulns.length !== 0}
                />
              </Col100>
            </Row>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={handleCloseModal}>
                    {translate.t("group.findings.report.modalClose")}
                  </Button>
                  <Button
                    disabled={
                      !(hasAcceptedVulns || hasRejectedVulns) ||
                      handlingAcceptation ||
                      confirmingZeroRisk ||
                      rejectingZeroRisk
                    }
                    onClick={handleUpdateTreatmentAcceptation}
                  >
                    {translate.t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </GenericForm>
        </Modal>
      </React.StrictMode>
    );
  };

export { HandleAcceptationModal };
