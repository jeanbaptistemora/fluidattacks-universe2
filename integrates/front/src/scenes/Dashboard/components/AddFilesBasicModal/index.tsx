import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React from "react";
import { mixed, object } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { IAddFilesBasicModalProps } from "scenes/Dashboard/components/AddFilesBasicModal/types";
import {
  ButtonToolbar,
  Col100,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikFileInput } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { isValidFileSize } from "utils/validations";

const addFilesBasicModal: React.FC<IAddFilesBasicModalProps> = (
  props: IAddFilesBasicModalProps
): JSX.Element => {
  const { isOpen, isUploading, onClose, onSubmit } = props;

  const MAX_FILE_SIZE: number = 5000;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);

  const addFilesModalSchema = object().shape({
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

export { IAddFilesBasicModalProps, addFilesBasicModal as AddFilesBasicModal };
