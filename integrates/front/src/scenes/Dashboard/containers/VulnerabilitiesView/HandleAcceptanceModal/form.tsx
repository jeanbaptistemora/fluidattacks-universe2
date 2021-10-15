import { Form, useFormikContext } from "formik";
import React, { useEffect } from "react";

import { AcceptedUndefinedTable } from "./AcceptedUndefinedTable";
import { onTreatmentChangeHelper } from "./helpers";
import { JustificationField } from "./JustificationField";
import { TreatmentField } from "./TreatmentField";
import { ZeroRiskTable } from "./ZeroRiskTable";

import { Button } from "components/Button";
import type {
  IFormValues,
  IHandleVulnerabilitiesAcceptanceModalFormProps,
} from "scenes/Dashboard/containers/VulnerabilitiesView/HandleAcceptanceModal/types";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const HandleAcceptanceModalForm: React.FC<IHandleVulnerabilitiesAcceptanceModalFormProps> =
  (props: IHandleVulnerabilitiesAcceptanceModalFormProps): JSX.Element => {
    const {
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
    } = props;

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
                  handlingAcceptance ||
                  confirmingZeroRisk ||
                  rejectingZeroRisk
                }
                onClick={submitForm}
              >
                {translate.t("confirmmodal.proceed")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Form>
    );
  };

export { HandleAcceptanceModalForm };
