import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React from "react";
import type { ConfigurableValidator } from "revalidate";
import { mixed, object, string } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
import {
  ButtonToolbar,
  Col100,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikFileInput, FormikTextArea } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  isValidFileSize,
  maxLength,
  validField,
  validTextField,
} from "utils/validations";

const MAX_LENGTH: number = 200;
const maxFileDescriptionLength: ConfigurableValidator = maxLength(MAX_LENGTH);

const addFilesModal: React.FC<IAddFilesModalProps> = (
  props: IAddFilesModalProps
): JSX.Element => {
  const { isOpen, isUploading, onClose, onSubmit } = props;

  const MAX_FILE_SIZE: number = 5000;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);

  const addFilesModalSchema = object().shape({
    description: string().required(translate.t("validations.required")),
    file: mixed()
      .required(translate.t("validations.required"))
      .test(
        "isValidFileName",
        translate.t("searchFindings.tabResources.invalidChars"),
        (value?: FileList): boolean => {
          if (value === undefined || _.isEmpty(value)) {
            return false;
          }
          const fileName: string = value[0].name;
          const name: string[] = fileName.split(".");
          const validCharacters: RegExp = /^[A-Za-z0-9!\-_.*'()&$@=;:+,?\s]*$/u;

          return name.length <= 2 && validCharacters.test(fileName);
        }
      ),
  });

  const initialValues = {
    description: "",
    file: undefined as unknown as FileList,
  };

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t("searchFindings.tabResources.modalFileTitle")}
        onEsc={onClose}
        open={isOpen}
      >
        <Formik
          enableReinitialize={true}
          initialValues={initialValues}
          name={"addFiles"}
          onSubmit={onSubmit}
          validationSchema={addFilesModalSchema}
        >
          {({ dirty }): React.ReactNode => (
            <Form>
              <div>
                <div>
                  <label>
                    <RequiredField>{"*"} </RequiredField>
                  </label>
                  <Field
                    component={FormikFileInput}
                    id={"file"}
                    name={"file"}
                    validate={maxFileSize}
                  />
                </div>
                <div>
                  <label>
                    <RequiredField>{"*"} </RequiredField>
                    {translate.t("searchFindings.tabResources.description")}
                  </label>
                  <Field
                    component={FormikTextArea}
                    name={"description"}
                    type={"text"}
                    validate={composeValidators([
                      validField,
                      maxFileDescriptionLength,
                      validTextField,
                    ])}
                  />
                </div>
              </div>
              {isUploading ? (
                <div>
                  {" "}
                  <br />
                  {translate.t("searchFindings.tabResources.uploadingProgress")}
                </div>
              ) : undefined}
              <hr />
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"file-add-cancel"} onClick={onClose}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty || isUploading}
                      id={"file-add-proceed"}
                      type={"submit"}
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

export { IAddFilesModalProps, addFilesModal as AddFilesModal };
