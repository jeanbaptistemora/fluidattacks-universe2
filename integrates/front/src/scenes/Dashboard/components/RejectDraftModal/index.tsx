import { Form, Formik } from "formik";
import type { FC } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { Checkbox, Label, TextArea } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { validTextField } from "utils/validations";

interface IRejectDraftModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { reasons: string[]; other: string }) => void;
}

const RejectDraftModal: FC<IRejectDraftModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IRejectDraftModalProps): JSX.Element => {
  const { t } = useTranslation();

  const draftRejectionReasons: Record<string, string> = {
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

  const rejectDraftValidations = object().shape({
    other: string().when("reasons", {
      is: (reasons: string[]): boolean => reasons.includes("OTHER"),
      otherwise: string(),
      then: string().required(t("validations.required")),
    }),
    reasons: array()
      .min(1, t("validations.someRequired"))
      .of(string().required(t("validations.required"))),
  });

  return (
    <StrictMode>
      <Modal
        minWidth={400}
        onClose={onClose}
        open={isOpen}
        title={t("group.drafts.reject.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            other: "",
            reasons: [],
          }}
          name={"rejectDraft"}
          onSubmit={onSubmit}
          validationSchema={rejectDraftValidations}
        >
          {({ dirty, isSubmitting, values }): JSX.Element => (
            <Form>
              <Gap disp={"block"} mv={5}>
                <Label required={true}>{t("group.drafts.reject.reason")}</Label>
                {Object.entries(draftRejectionReasons).map(
                  ([reason, explanation]): JSX.Element => (
                    <Checkbox
                      id={reason}
                      key={`reasons.${reason}`}
                      label={t(`group.drafts.reject.${reason.toLowerCase()}`)}
                      name={"reasons"}
                      tooltip={explanation}
                      value={reason}
                    />
                  )
                )}
                {(values.reasons as string[]).includes("OTHER") ? (
                  <TextArea
                    id={"reject-draft-other-reason"}
                    label={t("group.drafts.reject.otherReason")}
                    name={"other"}
                    required={true}
                    validate={validTextField}
                  />
                ) : undefined}
                <ModalConfirm
                  disabled={!dirty || isSubmitting}
                  id={"reject-draft-confirm"}
                  onCancel={onClose}
                />
              </Gap>
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export { RejectDraftModal };
