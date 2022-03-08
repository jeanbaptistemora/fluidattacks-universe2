import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React from "react";
import { mixed, object } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { IAddFilesBasicModalProps } from "scenes/Dashboard/components/AddFilesBasicModal/types";
import { RequiredField } from "styles/styledComponents";
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
        onClose={onClose}
        open={isOpen}
        title={translate.t("searchFindings.tabResources.modalFileTitle")}
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
              <div>
                <div>
                  <ModalFooter>
                    <Button
                      id={"file-add-cancel"}
                      onClick={onClose}
                      variant={"secondary"}
                    >
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={!dirty || isUploading}
                      id={"file-add-proceed"}
                      type={"submit"}
                      variant={"primary"}
                    >
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ModalFooter>
                </div>
              </div>
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { IAddFilesBasicModalProps, addFilesBasicModal as AddFilesBasicModal };
