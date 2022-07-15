import { Field, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { Modal, ModalConfirm } from "components/Modal";
import { Tooltip } from "components/Tooltip";
import { Alert, ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { required } from "utils/validations";

interface IDeleteGroupModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string; reason: string }) => void;
}

const DeleteGroupModal: React.FC<IDeleteGroupModalProps> = ({
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
    <React.StrictMode>
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
            <React.Fragment>
              <ControlLabel>
                {t("searchFindings.servicesTable.deleteGroup.warningTitle")}
              </ControlLabel>
              <Alert>
                {t("searchFindings.servicesTable.deleteGroup.warningBody")}
              </Alert>
              <FormGroup>
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
              </FormGroup>
              <FormGroup>
                <ControlLabel>
                  {t("searchFindings.servicesTable.deleteGroup.reason.title")}
                </ControlLabel>
                <Tooltip
                  id={"searchFindings.servicesTable.deleteGroup.reason.tooltip"}
                  place={"top"}
                  tip={t(
                    "searchFindings.servicesTable.deleteGroup.reason.tooltip"
                  )}
                >
                  <FormGroup>
                    <Field component={FormikDropdown} name={"reason"}>
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
                      <option value={"MIGRATION"}>
                        {t(
                          "searchFindings.servicesTable.deleteGroup.reason.migration"
                        )}
                      </option>
                      <option value={"OTHER"}>
                        {t(
                          "searchFindings.servicesTable.deleteGroup.reason.other"
                        )}
                      </option>
                    </Field>
                  </FormGroup>
                </Tooltip>
              </FormGroup>
              <ModalConfirm
                disabled={!dirty || !isValid}
                onCancel={onClose}
                onConfirm={submitForm}
              />
            </React.Fragment>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export { DeleteGroupModal };
