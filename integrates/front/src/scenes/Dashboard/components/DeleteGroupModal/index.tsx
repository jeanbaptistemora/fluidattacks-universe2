import { Field, Formik } from "formik";
import type { FC } from "react";
import React, { Fragment, StrictMode } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText, FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_LENGTH_VALIDATOR = 250;
const maxLength250 = maxLength(MAX_LENGTH_VALIDATOR);

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: {
    comments: string;
    confirmation: string;
    reason: string;
  }) => void;
}

const DeleteGroupModal: FC<IDeleteGroupModalProps> = ({
  groupName,
  isOpen,
  onClose,
  onSubmit,
}: IDeleteGroupModalProps): JSX.Element => {
  const { t } = useTranslation();

  function formValidations(values: { confirmation: string; reason: string }): {
    confirmation?: string;
    reason?: string;
  } {
    return values.confirmation === groupName
      ? {}
      : {
          confirmation: t(
            "searchFindings.servicesTable.errors.expectedGroupName",
            { groupName }
          ),
        };
  }

  return (
    <StrictMode>
      <Modal
        open={isOpen}
        title={t("searchFindings.servicesTable.deleteGroup.deleteGroup")}
      >
        <Formik
          initialValues={{
            comments: "",
            confirmation: "",
            reason: "NO_SYSTEM",
          }}
          name={"removeGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
        >
          {({ submitForm, isValid, dirty }): JSX.Element => (
            <Fragment>
              <ControlLabel>
                {t("searchFindings.servicesTable.deleteGroup.warningTitle")}
              </ControlLabel>
              <Alert>
                {t("searchFindings.servicesTable.deleteGroup.warningBody")}
              </Alert>
              <ControlLabel>
                {t("searchFindings.servicesTable.deleteGroup.typeGroupName")}
              </ControlLabel>
              <Field
                component={FormikText}
                name={"confirmation"}
                placeholder={groupName.toLowerCase()}
                type={"text"}
                validate={required}
              />
              <Select
                label={t(
                  "searchFindings.servicesTable.deleteGroup.reason.title"
                )}
                name={"reason"}
                tooltip={t(
                  "searchFindings.servicesTable.deleteGroup.reason.tooltip"
                )}
              >
                <option value={"NO_SYSTEM"}>
                  {t(
                    "searchFindings.servicesTable.deleteGroup.reason.noSystem"
                  )}
                </option>
                <option value={"NO_SECTST"}>
                  {t(
                    "searchFindings.servicesTable.deleteGroup.reason.noSectst"
                  )}
                </option>
                <option value={"DIFF_SECTST"}>
                  {t(
                    "searchFindings.servicesTable.deleteGroup.reason.diffSectst"
                  )}
                </option>
                <option value={"RENAME"}>
                  {t("searchFindings.servicesTable.deleteGroup.reason.rename")}
                </option>
                <option value={"MIGRATION"}>
                  {t(
                    "searchFindings.servicesTable.deleteGroup.reason.migration"
                  )}
                </option>
                <option value={"OTHER"}>
                  {t("searchFindings.servicesTable.deleteGroup.reason.other")}
                </option>
              </Select>
              <FormGroup>
                <Text mb={2}>
                  {t("searchFindings.servicesTable.modal.observations")}
                </Text>
                <Field
                  component={FormikTextArea}
                  name={"comments"}
                  placeholder={t(
                    "searchFindings.servicesTable.modal.observationsPlaceholder"
                  )}
                  type={"text"}
                  validate={composeValidators([validTextField, maxLength250])}
                />
              </FormGroup>
              <ModalConfirm
                disabled={!dirty || !isValid}
                onCancel={onClose}
                onConfirm={submitForm}
              />
            </Fragment>
          )}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export { DeleteGroupModal };
