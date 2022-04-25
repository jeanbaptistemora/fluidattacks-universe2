import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";
import { mixed, object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import type { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
import { RequiredField } from "styles/styledComponents";
import { FormikFileInput, FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  isValidFileSize,
  maxLength,
  validField,
  validTextField,
} from "utils/validations";

const MAX_LENGTH: number = 200;
const maxFileDescriptionLength: ConfigurableValidator = maxLength(MAX_LENGTH);

const AddFilesModal: React.FC<IAddFilesModalProps> = ({
  isOpen,
  isUploading,
  onClose,
  onSubmit,
}: IAddFilesModalProps): JSX.Element => {
  const { t } = useTranslation();

  const MAX_FILE_SIZE: number = 5000;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);

  const addFilesModalSchema = object().shape({
    description: string().required(t("validations.required")),
    file: mixed()
      .required(t("validations.required"))
      .test(
        "isValidFileName",
        t("searchFindings.tabResources.invalidChars"),
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
        onClose={onClose}
        open={isOpen}
        title={t("searchFindings.tabResources.modalFileTitle")}
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
                    {t("searchFindings.tabResources.description")}
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
                  {t("searchFindings.tabResources.uploadingProgress")}
                </div>
              ) : undefined}
              <ModalFooter>
                <Button
                  id={"file-add-cancel"}
                  onClick={onClose}
                  variant={"secondary"}
                >
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty || isUploading}
                  id={"file-add-proceed"}
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

export type { IAddFilesModalProps };
export { AddFilesModal };
