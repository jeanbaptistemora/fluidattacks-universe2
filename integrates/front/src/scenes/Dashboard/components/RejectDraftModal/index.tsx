import { Field, Form, Formik } from "formik";
import type { FC } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { FormikTextArea } from "utils/forms/fields";
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
              <Gap disp={"block"} mv={5}>
                <Select
                  id={"reject-draft-reason"}
                  label={
                    <React.Fragment>
                      <Text disp={"inline"} tone={"red"}>
                        {"* "}
                      </Text>
                      {t("group.drafts.reject.reason")}
                    </React.Fragment>
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
                  <React.Fragment>
                    <Text mb={1}>
                      <Text disp={"inline"} tone={"red"}>
                        {"* "}
                      </Text>
                      {t("group.drafts.reject.otherReason")}
                    </Text>
                    <Field
                      component={FormikTextArea}
                      id={"reject-draft-other-reason"}
                      name={"other"}
                      type={"text"}
                      validate={validTextField}
                    />
                  </React.Fragment>
                ) : undefined}
                <ModalConfirm
                  disabled={!dirty}
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
