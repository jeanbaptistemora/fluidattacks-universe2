import { Form, Formik } from "formik";
import type { FC } from "react";
import React, { Fragment, StrictMode } from "react";
import { useTranslation } from "react-i18next";

import { Input, InputArray, Label } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { composeValidators, required, validTag } from "utils/validations";

interface IAddTagsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { tags: string[] }) => void;
}

function renderTagsFields(fieldName: string): JSX.Element {
  return (
    <Fragment>
      <Label required={true}>{"Tag"}</Label>
      <Input
        name={fieldName}
        type={"text"}
        validate={composeValidators([required, validTag])}
      />
    </Fragment>
  );
}

const AddTagsModal: FC<IAddTagsModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IAddTagsModalProps): JSX.Element => {
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
            tags: [""],
          }}
          name={"addTags"}
          onSubmit={onSubmit}
        >
          {({ dirty }): JSX.Element => (
            <Form>
              <InputArray initValue={""} name={"tags"}>
                {renderTagsFields}
              </InputArray>
              <ModalConfirm
                disabled={!dirty}
                id={"portfolio-add-confirm"}
                onCancel={onClose}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddTagsModalProps };
export { AddTagsModal };
