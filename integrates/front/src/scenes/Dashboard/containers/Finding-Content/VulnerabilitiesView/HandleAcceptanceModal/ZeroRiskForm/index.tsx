import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IFormValues, IZeroRiskFormProps } from "./types";

import { getVulnsPendingOfAcceptance } from "../../utils";
import { AcceptedUndefinedTable } from "../AcceptedUndefinedTable";
import {
  confirmZeroRiskProps,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  rejectZeroRiskProps,
} from "../helpers";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "../queries";
import type { IVulnDataAttr } from "../types";
import { TextArea } from "components/Input";
import { ModalConfirm } from "components/Modal";

const ZeroRiskForm: React.FC<IZeroRiskFormProps> = ({
  groupName,
  findingId,
  onCancel,
  refetchData,
  vulnerabilities,
}: IZeroRiskFormProps): JSX.Element => {
  const { t } = useTranslation();

  // State
  const [acceptanceVulnerabilities, setAcceptanceVulnerabilities] = useState<
    IVulnDataAttr[]
  >(getVulnsPendingOfAcceptance(vulnerabilities));
  const [confirmedVulnerabilities, setConfirmedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);
  const [rejectedVulnerabilities, setRejectedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);

  // GraphQL operations
  const [confirmZeroRisk, { loading: confirmingZeroRisk }] = useMutation(
    CONFIRM_VULNERABILITIES_ZERO_RISK,
    confirmZeroRiskProps(refetchData, onCancel, findingId)
  );
  const [rejectZeroRisk, { loading: rejectingZeroRisk }] = useMutation(
    REJECT_VULNERABILITIES_ZERO_RISK,
    rejectZeroRiskProps(refetchData, onCancel, groupName, findingId)
  );

  // Handle actions
  const handleSubmit = useCallback(
    (formValues: IFormValues): void => {
      isConfirmZeroRiskSelectedHelper(
        true,
        confirmZeroRisk,
        confirmedVulnerabilities,
        formValues
      );
      isRejectZeroRiskSelectedHelper(
        true,
        rejectZeroRisk,
        formValues,
        rejectedVulnerabilities
      );
    },
    [
      confirmZeroRisk,
      confirmedVulnerabilities,
      rejectZeroRisk,
      rejectedVulnerabilities,
    ]
  );

  // Side effects
  useEffect((): void => {
    setConfirmedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "APPROVED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
    setRejectedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "REJECTED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
  }, [acceptanceVulnerabilities]);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ justification: "" }}
      name={"zeroRiskForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        justification: string().required(t("validations.required")),
      })}
    >
      <Form id={"zeroRiskForm"}>
        <div className={"ph1-5"}>
          <AcceptedUndefinedTable
            acceptanceVulns={acceptanceVulnerabilities}
            isAcceptedUndefinedSelected={true}
            setAcceptanceVulns={setAcceptanceVulnerabilities}
          />
          <br />
          <TextArea
            label={t(
              "searchFindings.tabDescription.remediationModal.observations"
            )}
            name={"justification"}
            required={true}
          />
        </div>
        <br />
        <ModalConfirm
          disabled={
            (confirmedVulnerabilities.length === 0 &&
              rejectedVulnerabilities.length === 0) ||
            confirmingZeroRisk ||
            rejectingZeroRisk
          }
          onCancel={onCancel}
        />
      </Form>
    </Formik>
  );
};

export { ZeroRiskForm };
