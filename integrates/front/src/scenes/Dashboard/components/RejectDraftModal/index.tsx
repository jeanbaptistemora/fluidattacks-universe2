import { Field, Form, Formik } from "formik";
import type { FC } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";

import { Modal, ModalConfirm } from "components/Modal";
import { FormikDropdown, FormikText } from "utils/forms/fields";

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

  return (
    <StrictMode>
      <Modal
        minWidth={400}
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabIndicators.tags.modalTitle")}
      >
        <Formik
          initialValues={{
            other: "",
            reason: "",
          }}
          name={"addTags"}
          onSubmit={onSubmit}
        >
          {({ dirty }): JSX.Element => (
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
              <Field
                component={FormikText}
                key={"other"}
                label={t("group.drafts.reject.otherReason")}
                name={"other"}
                type={"checkbox"}
                value={"other"}
              />
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
