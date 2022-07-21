import { Field, Form, Formik } from "formik";
import type { FieldValidator } from "formik";
import _ from "lodash";
import type { FC, ReactNode } from "react";
import React, { StrictMode } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";
import { mixed, object, string } from "yup";

import { Alert } from "components/Alert";
import { Label } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import type { IAddFilesModalProps } from "scenes/Dashboard/components/AddFilesModal/types";
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

const AddFilesModal: FC<IAddFilesModalProps> = ({
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
    <StrictMode>
      <Modal
        minWidth={400}
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
          {({ dirty }): ReactNode => (
            <Form>
              <Gap disp={"block"} mh={0} mv={12}>
                <div>
                  <Label required={true} />
                  <Field
                    component={FormikFileInput}
                    id={"file"}
                    name={"file"}
                    validate={maxFileSize}
                  />
                </div>
                <div>
                  <Label required={true}>
                    {t("searchFindings.tabResources.description")}
                  </Label>
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
                {isUploading ? (
                  <Alert variant={"info"}>
                    {t("searchFindings.tabResources.uploadingProgress")}
                  </Alert>
                ) : undefined}
              </Gap>
              <ModalConfirm
                disabled={!dirty || isUploading}
                onCancel={onClose}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export type { IAddFilesModalProps };
export { AddFilesModal };
