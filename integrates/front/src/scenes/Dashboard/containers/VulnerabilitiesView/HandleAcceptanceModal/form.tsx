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

const HandleAcceptationModalForm: React.FC<IHandleVulnerabilitiesAcceptanceModalFormProps> =
  (props: IHandleVulnerabilitiesAcceptanceModalFormProps): JSX.Element => {
    const {
      acceptanceVulnerabilities: acceptationVulns,
      acceptedVulnerabilities: acceptedVulns,
      confirmingZeroRisk,
      handleCloseModal,
      handlingAcceptation,
      hasAcceptedVulns,
      hasRejectedVulns,
      rejectedVulnerabilities: rejectedVulns,
      rejectingZeroRisk,
      setAcceptationVulns,
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
        setAcceptationVulns,
        isConfirmRejectZeroRiskSelected
      );
    };
    useEffect(onTreatmentChange, [
      isAcceptedUndefinedSelected,
      isConfirmRejectZeroRiskSelected,
      setAcceptationVulns,
      vulns,
    ]);

    return (
      <Form id={"updateTreatmentAcceptation"}>
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
              acceptanceVulns={acceptationVulns}
              isConfirmRejectZeroRiskSelected={isConfirmRejectZeroRiskSelected}
              setAcceptanceVulns={setAcceptationVulns}
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

export { HandleAcceptationModalForm };
