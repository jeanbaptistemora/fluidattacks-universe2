/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Form, useFormikContext } from "formik";
import React, { useEffect } from "react";

import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import { onTreatmentChangeHelper } from "./helpers";
import { JustificationField } from "./JustificationField";
import { TreatmentField } from "./TreatmentField";
import { ZeroRiskTable } from "./ZeroRiskTable";

import { ModalConfirm } from "components/Modal";
import type {
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/types";
import { Col100, Col50, Row } from "styles/styledComponents";

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
    vulns,
  }: IHandleVulnerabilitiesAcceptanceModalFormProps): JSX.Element => {
    const { values, submitForm } = useFormikContext<IFormValues>();

    const isAcceptedUndefinedSelected: boolean =
      values.treatment === "ACCEPTED_UNDEFINED";
    const isConfirmRejectZeroRiskSelected: boolean =
      values.treatment === "CONFIRM_REJECT_ZERO_RISK";

    // Side effects
    const onTreatmentChange: () => void = (): void => {
      onTreatmentChangeHelper(
        isAcceptedUndefinedSelected,
        vulns,
        setAcceptanceVulns,
        isConfirmRejectZeroRiskSelected
      );
    };
    useEffect(onTreatmentChange, [
      isAcceptedUndefinedSelected,
      isConfirmRejectZeroRiskSelected,
      setAcceptanceVulns,
      vulns,
    ]);

    return (
      <Form id={"updateTreatmentAcceptance"}>
        <Row>
          <Col50>
            <TreatmentField />
          </Col50>
        </Row>
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
