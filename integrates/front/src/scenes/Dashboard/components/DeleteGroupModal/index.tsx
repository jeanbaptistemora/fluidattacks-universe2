import { Field, Formik } from "formik";
import type { FC } from "react";
import React, { Fragment, StrictMode } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { required } from "utils/validations";

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string; reason: string }) => void;
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
