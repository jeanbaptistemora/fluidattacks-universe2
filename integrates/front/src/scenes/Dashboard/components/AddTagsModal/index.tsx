import { Field, Form, Formik } from "formik";
import React from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikArrayField, FormikText } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
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

const AddTagsModal: React.FC<IAddTagsModalProps> = (
  props: IAddTagsModalProps
): JSX.Element => {
  const { isOpen, onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "searchFindings.tabIndicators.tags.modalTitle"
        )}
        onClose={onClose}
        open={isOpen}
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
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button
                      id={"portfolio-add-cancel"}
                      onClick={onClose}
                      variant={"secondary"}
                    >
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty}
                      id={"portfolio-add-proceed"}
                      type={"submit"}
                      variant={"primary"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { AddTagsModal, IAddTagsModalProps };
