import { Field, Form, Formik } from "formik";
import type { FC } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IRejectDraftModalProps } from "./types";

import { Label, Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { FormikTextArea } from "utils/forms/fields";
import { validTextField } from "utils/validations";

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
    reason: string().required(t("validations.required")),
  });

  return (
    <StrictMode>
      <Modal
        minWidth={500}
        onClose={onClose}
        open={isOpen}
        title={t("group.drafts.reject.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            other: "",
            reason: "",
          }}
          name={"rejectDraft"}
          onSubmit={onSubmit}
          validationSchema={validations}
        >
          {({ dirty, isSubmitting, values }): JSX.Element => (
            <Form>
              <Gap disp={"block"} mv={5}>
                <Select
                  id={"reject-draft-reason"}
                  label={
                    <Label required={true}>
                      {t("group.drafts.reject.reason")}
                    </Label>
                  }
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
                </Select>
                {values.reason === "OTHER" ? (
                  <div>
                    <Label required={true}>
                      {t("group.drafts.reject.otherReason")}
                    </Label>
                    <Field
                      component={FormikTextArea}
                      id={"reject-draft-other-reason"}
                      name={"other"}
                      type={"text"}
                      validate={validTextField}
                    />
                  </div>
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
