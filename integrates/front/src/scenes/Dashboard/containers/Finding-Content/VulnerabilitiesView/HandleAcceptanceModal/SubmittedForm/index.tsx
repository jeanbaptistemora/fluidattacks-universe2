import { useMutation } from "@apollo/client";
import { Form, Formik } from "formik";
import React, { Fragment, useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { SubmittedTable } from "./SubmittedTable";
import type { IFormValues, ISubmittedFormProps } from "./types";

import { getSubmittedVulns } from "../../utils";
import {
  confirmVulnerabilityHelper,
  confirmVulnerabilityProps,
  rejectVulnerabilityHelper,
  rejectVulnerabilityProps,
} from "../helpers";
import { CONFIRM_VULNERABILITIES, REJECT_VULNERABILITIES } from "../queries";
import type { IVulnDataAttr } from "../types";
import { Checkbox, Label, TextArea } from "components/Input";
import { Gap } from "components/Layout";
import { ModalConfirm } from "components/Modal";

const SubmittedForm: React.FC<ISubmittedFormProps> = ({
  groupName,
  findingId,
  onCancel,
  refetchData,
  vulnerabilities,
}: ISubmittedFormProps): JSX.Element => {
  const { t } = useTranslation();

  const rejectionReasons: Record<string, string> = {
    CONSISTENCY:
      "There are consistency issues with the vulnerabilities, the severity " +
      "or the evidence",
    EVIDENCE: "The evidence is insufficient",
    NAMING:
      "The vulnerabilities should be submitted under another Finding type",
    OMISSION: "More data should be gathered before submission",
    SCORING: "Faulty severity scoring",
    WRITING: "The writing could be improved",
    // eslint-disable-next-line sort-keys
    OTHER: "Another reason",
  };

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
  const [rejectVulnerability, { loading: rejectingVulnerability }] =
    useMutation(
      REJECT_VULNERABILITIES,
      rejectVulnerabilityProps(refetchData, onCancel, findingId)
    );

  // Handle actions
  const handleSubmit = useCallback(
    (formValues: IFormValues): void => {
      confirmVulnerabilityHelper(
        true,
        confirmVulnerability,
        confirmedVulnerabilities
      );
      rejectVulnerabilityHelper(
        true,
        rejectVulnerability,
        {
          otherReason: formValues.rejectionReasons.includes("OTHER")
            ? formValues.otherRejectionReason
            : undefined,
          reasons: formValues.rejectionReasons,
        },
        rejectedVulnerabilities
      );
    },
    [
      confirmVulnerability,
      confirmedVulnerabilities,
      rejectVulnerability,
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
      initialValues={{
        otherRejectionReason: undefined,
        rejectionReasons: [] as string[],
      }}
      name={"submittedForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        otherRejectionReason: string().when("rejectionReasons", {
          is: (reasons: string[]): boolean => reasons.includes("OTHER"),
          otherwise: string(),
          then: string().required(t("validations.required")),
        }),
        rejectionReasons: array()
          .min(1, t("validations.someRequired"))
          .of(string().required(t("validations.required"))),
      })}
    >
      {({ values }): JSX.Element => {
        return (
          <Form id={"submittedForm"}>
            <SubmittedTable
              acceptanceVulns={acceptanceVulnerabilities}
              isConfirmRejectVulnerabilitySelected={true}
              setAcceptanceVulns={setAcceptanceVulnerabilities}
            />
            {rejectedVulnerabilities.length === 0 ? undefined : (
              <Fragment>
                <br />
                <Gap disp={"block"} mv={6}>
                  <Label required={true}>
                    {t("group.drafts.reject.reason")}
                  </Label>
                  {Object.entries(rejectionReasons).map(
                    ([reason, explanation]): JSX.Element => (
                      <Checkbox
                        id={reason}
                        key={`rejectionReasons.${reason}`}
                        label={t(`group.drafts.reject.${reason.toLowerCase()}`)}
                        name={"rejectionReasons"}
                        tooltip={explanation}
                        value={reason}
                      />
                    )
                  )}
                  {values.rejectionReasons.includes("OTHER") ? (
                    <TextArea
                      id={"reject-draft-other-reason"}
                      label={t("group.drafts.reject.otherReason")}
                      name={"otherRejectionReason"}
                      required={true}
                    />
                  ) : undefined}
                </Gap>
              </Fragment>
            )}
            <br />
            <ModalConfirm
              disabled={
                (confirmedVulnerabilities.length === 0 &&
                  rejectedVulnerabilities.length === 0) ||
                confirmingVulnerability ||
                rejectingVulnerability
              }
              onCancel={onCancel}
            />
          </Form>
        );
      }}
    </Formik>
  );
};

export { SubmittedForm };
