import { Form, useFormikContext } from "formik";
import React, { useEffect } from "react";

import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import { onTreatmentChangeHelper } from "./helpers";
import { JustificationField } from "./JustificationField";
import { SubmittedTable } from "./SubmittedTable";
import { ZeroRiskTable } from "./ZeroRiskTable";

import { ModalConfirm } from "components/Modal";
import type {
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
} from "scenes/Dashboard/containers/Finding-Content/VulnerabilitiesView/HandleAcceptanceModal/types";
import { Col100, Row } from "styles/styledComponents";

const HandleAcceptanceModalForm: React.FC<IHandleVulnerabilitiesAcceptanceModalFormProps> =
  ({
    acceptanceVulnerabilities,
    acceptedVulnerabilities,
    confirmingZeroRisk,
    handleCloseModal,
    handlingAcceptance,
    hasAcceptedVulns,
    hasRejectedVulns,
    rejectedVulnerabilities,
    rejectingZeroRisk,
    setAcceptanceVulns,
    treatment,
    vulns,
  }: IHandleVulnerabilitiesAcceptanceModalFormProps): JSX.Element => {
    const { submitForm } = useFormikContext<IFormValues>();

    const isAcceptedUndefinedSelected: boolean =
      treatment === "ACCEPTED_UNDEFINED";
    const isConfirmRejectZeroRiskSelected: boolean =
      treatment === "CONFIRM_REJECT_ZERO_RISK";
    const isConfirmRejectVulnerabilitySelected: boolean =
      treatment === "CONFIRM_REJECT_VULNERABILITY";

    // Side effects
    const onTreatmentChange: () => void = (): void => {
      onTreatmentChangeHelper(
        isAcceptedUndefinedSelected,
        vulns,
        setAcceptanceVulns,
        isConfirmRejectZeroRiskSelected,
        isConfirmRejectVulnerabilitySelected
      );
    };
    useEffect(onTreatmentChange, [
      isAcceptedUndefinedSelected,
      isConfirmRejectZeroRiskSelected,
      isConfirmRejectVulnerabilitySelected,
      setAcceptanceVulns,
      vulns,
    ]);

    return (
      <Form id={"updateTreatmentAcceptance"}>
        <Row>
          <Col100>
            <AcceptedUndefinedTable
              acceptanceVulns={acceptanceVulnerabilities}
              isAcceptedUndefinedSelected={isAcceptedUndefinedSelected}
              setAcceptanceVulns={setAcceptanceVulns}
            />
          </Col100>
        </Row>
        <Row>
          <Col100>
            <ZeroRiskTable
              acceptanceVulns={acceptanceVulnerabilities}
              isConfirmRejectZeroRiskSelected={isConfirmRejectZeroRiskSelected}
              setAcceptanceVulns={setAcceptanceVulns}
            />
          </Col100>
        </Row>
        <Row>
          <Col100>
            <SubmittedTable
              acceptanceVulns={acceptanceVulnerabilities}
              isConfirmRejectVulnerabilitySelected={
                isConfirmRejectVulnerabilitySelected
              }
              setAcceptanceVulns={setAcceptanceVulns}
            />
          </Col100>
        </Row>
        <Row>
          <Col100>
            <JustificationField
              isConfirmZeroRiskSelected={acceptedVulnerabilities.length !== 0}
              isRejectZeroRiskSelected={rejectedVulnerabilities.length !== 0}
            />
          </Col100>
        </Row>
        <ModalConfirm
          disabled={
            !(hasAcceptedVulns || hasRejectedVulns) ||
            handlingAcceptance ||
            confirmingZeroRisk ||
            rejectingZeroRisk
          }
          onCancel={handleCloseModal}
          onConfirm={submitForm}
        />
      </Form>
    );
  };

export { HandleAcceptanceModalForm };
