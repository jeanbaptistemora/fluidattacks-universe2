import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikArrayField, FormikText } from "utils/forms/fields";
import { composeValidators, required, validTag } from "utils/validations";

interface IAddTagsModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { tags: string[] }) => void;
}

function renderTagsFields(fieldName: string): JSX.Element {
  return (
    <React.Fragment>
      <ControlLabel>
        <RequiredField>{"* "}</RequiredField>
        {"Tag"}
      </ControlLabel>
      <Field
        component={FormikText}
        name={fieldName}
        type={"text"}
        validate={composeValidators([required, validTag])}
      />
    </React.Fragment>
  );
}

const AddTagsModal: React.FC<IAddTagsModalProps> = ({
  isOpen,
  onClose,
  onSubmit,
}: IAddTagsModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <React.StrictMode>
      <Modal
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
              <FormikArrayField
                allowEmpty={false}
                initialValue={""}
                name={"tags"}
              >
                {renderTagsFields}
              </FormikArrayField>
              <ModalFooter>
                <Button
                  id={"portfolio-add-cancel"}
                  onClick={onClose}
                  variant={"secondary"}
                >
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty}
                  id={"portfolio-add-proceed"}
                  type={"submit"}
                  variant={"primary"}
                >
                  {t("confirmmodal.proceed")}
                </Button>
              </ModalFooter>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddTagsModal, IAddTagsModalProps };
