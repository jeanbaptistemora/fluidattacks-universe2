import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";
import { mixed, object } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import type { IAddFilesBasicModalProps } from "scenes/Dashboard/components/AddFilesBasicModal/types";
import { RequiredField } from "styles/styledComponents";
import { FormikFileInput } from "utils/forms/fields";
import { isValidFileSize } from "utils/validations";

const AddFilesBasicModal: React.FC<IAddFilesBasicModalProps> = ({
  isOpen,
  isUploading,
  onClose,
  onSubmit,
}: IAddFilesBasicModalProps): JSX.Element => {
  const { t } = useTranslation();

  const MAX_FILE_SIZE: number = 5000;
  const maxFileSize: FieldValidator = isValidFileSize(MAX_FILE_SIZE);

  const addFilesModalSchema = object().shape({
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

export type { IAddFilesBasicModalProps };
export { AddFilesBasicModal };
