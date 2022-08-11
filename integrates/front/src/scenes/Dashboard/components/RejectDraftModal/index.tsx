import { Field, Form, Formik } from "formik";
import type { FC } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { validTextField } from "utils/validations";

interface IRejectDraftModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { reason: string; other: string }) => void;
}

const draftRejectionReason: string[] = [
  "CONSISTENCY",
  "EVIDENCE",
  "NAMING",
  "OMISSION",
  "OTHER",
  "SCORING",
  "WRITING",
];

const RejectDraftModal: FC<IRejectDraftModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IRejectDraftModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    other: string().when("reason", {
      is: "OTHER",
      then: string().required(t("validations.required")),
    }),
    reason: string().required(),
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
          initialValues={{
            other: "",
            reason: "",
          }}
          name={"rejectDraft"}
          onSubmit={onSubmit}
          validationSchema={validations}
        >
          {({ dirty, values }): JSX.Element => (
            <Form>
              <Field
                component={FormikDropdown}
                key={"reason"}
                label={t("group.drafts.reject.otherReason")}
                name={"reason"}
              >
                <option value={""}>{""}</option>
                {draftRejectionReason.map(
                  (reason): JSX.Element => (
                    <option key={reason} value={reason}>
                      {t(`group.drafts.reject.${reason.toLowerCase()}`)}
                    </option>
                  )
                )}
              </Field>
              {values.reason === "OTHER" ? (
                <Field
                  component={FormikText}
                  key={"other"}
                  label={t("group.drafts.reject.otherReason")}
                  name={"other"}
                  type={"text"}
                  validate={validTextField}
                  value={"other"}
                />
              ) : undefined}
              <ModalConfirm
                disabled={!dirty}
                id={"reject-draft-confirm"}
                onCancel={onClose}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export { RejectDraftModal };
