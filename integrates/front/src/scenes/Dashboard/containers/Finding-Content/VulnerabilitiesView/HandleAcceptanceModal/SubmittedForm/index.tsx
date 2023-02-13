import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IFormValues, ISubmittedFormProps } from "./types";

import { getSubmittedVulns } from "../../utils";
import {
  confirmVulnerabilityHelper,
  confirmVulnerabilityProps,
} from "../helpers";
import { CONFIRM_VULNERABILITIES } from "../queries";
import { SubmittedTable } from "../SubmittedTable";
import type { IVulnDataAttr } from "../types";
import { ModalConfirm } from "components/Modal";

const SubmittedForm: React.FC<ISubmittedFormProps> = ({
  groupName,
  findingId,
  onCancel,
  refetchData,
  vulnerabilities,
}: ISubmittedFormProps): JSX.Element => {
  const { t } = useTranslation();

  // State
  const [acceptanceVulnerabilities, setAcceptanceVulnerabilities] = useState<
    IVulnDataAttr[]
  >(getSubmittedVulns(vulnerabilities));
  const [confirmedVulnerabilities, setConfirmedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);
  const [rejectedVulnerabilities, setRejectedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);

  // GraphQL operations
  const [confirmVulnerability, { loading: confirmingVulnerability }] =
    useMutation(
      CONFIRM_VULNERABILITIES,
      confirmVulnerabilityProps(refetchData, onCancel, groupName, findingId)
    );

  // Handle actions
  const handleSubmit = useCallback(
    (_formValues: IFormValues): void => {
      confirmVulnerabilityHelper(
        true,
        confirmVulnerability,
        confirmedVulnerabilities
      );
    },
    [confirmVulnerability, confirmedVulnerabilities]
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
      name={"submittedForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        justification: string().when([], {
          is: (): boolean => rejectedVulnerabilities.length > 0,
          otherwise: string().notRequired(),
          then: string().required(t("validations.required")),
        }),
      })}
    >
      <Form id={"submittedForm"}>
        <div className={"ph1-5"}>
          <SubmittedTable
            acceptanceVulns={acceptanceVulnerabilities}
            isConfirmRejectVulnerabilitySelected={true}
            setAcceptanceVulns={setAcceptanceVulnerabilities}
          />
        </div>
        <br />
        <ModalConfirm
          disabled={
            (confirmedVulnerabilities.length === 0 &&
              rejectedVulnerabilities.length === 0) ||
            confirmingVulnerability
          }
          onCancel={onCancel}
        />
      </Form>
    </Formik>
  );
};

export { SubmittedForm };
