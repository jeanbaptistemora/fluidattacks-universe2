import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IFormValues, IPermanentlyAcceptedFormProps } from "./types";

import { getVulnsPendingOfAcceptance } from "../../utils";
import { AcceptedUndefinedTable } from "../AcceptedUndefinedTable";
import { acceptanceProps, isAcceptedUndefinedSelectedHelper } from "../helpers";
import { HANDLE_VULNS_ACCEPTANCE } from "../queries";
import type { IVulnDataAttr } from "../types";
import { TextArea } from "components/Input";
import { ModalConfirm } from "components/Modal";

const PermanentlyAcceptedForm: React.FC<IPermanentlyAcceptedFormProps> = ({
  findingId,
  onCancel,
  refetchData,
  vulnerabilities,
}: IPermanentlyAcceptedFormProps): JSX.Element => {
  const { t } = useTranslation();

  // State
  const [acceptanceVulnerabilities, setAcceptanceVulnerabilities] = useState<
    IVulnDataAttr[]
  >(getVulnsPendingOfAcceptance(vulnerabilities));
  const [acceptedVulnerabilities, setAcceptedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);
  const [rejectedVulnerabilities, setRejectedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);

  // GraphQL operations
  const [handleAcceptance, { loading }] = useMutation(
    HANDLE_VULNS_ACCEPTANCE,
    acceptanceProps(refetchData, onCancel, findingId)
  );

  // Handle actions
  const handleSubmit = useCallback(
    (formValues: IFormValues): void => {
      isAcceptedUndefinedSelectedHelper(
        true,
        handleAcceptance,
        acceptedVulnerabilities,
        formValues,
        rejectedVulnerabilities
      );
    },
    [acceptedVulnerabilities, handleAcceptance, rejectedVulnerabilities]
  );

  // Side effects
  useEffect((): void => {
    setAcceptedVulnerabilities(
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
      name={"permanentlyAcceptedForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        justification: string().required(t("validations.required")),
      })}
    >
      <Form id={"permanentlyAcceptedForm"}>
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
        <br />
        <ModalConfirm
          disabled={
            (acceptedVulnerabilities.length === 0 &&
              rejectedVulnerabilities.length === 0) ||
            loading
          }
          onCancel={onCancel}
        />
      </Form>
    </Formik>
  );
};

export { PermanentlyAcceptedForm };
