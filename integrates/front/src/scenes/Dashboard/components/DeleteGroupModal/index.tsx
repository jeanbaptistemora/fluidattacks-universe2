import { Formik } from "formik";
import type { FC } from "react";
import React, { Fragment, StrictMode, useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import { Input, Select, TextArea } from "components/Input";
import { Row } from "components/Layout/Row";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel } from "styles/styledComponents";
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

  const formValidations = useCallback(
    (values: {
      confirmation: string;
      reason: string;
    }): {
      confirmation?: string;
      reason?: string;
    } => {
      return values.confirmation === groupName
        ? {}
        : {
            confirmation: t(
              "searchFindings.servicesTable.errors.expectedGroupName",
              { groupName }
            ),
          };
    },
    [groupName, t]
  );

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
              <Row>
                <ControlLabel>
                  {t("searchFindings.servicesTable.deleteGroup.warningTitle")}
                </ControlLabel>
                <Alert>
                  {t("searchFindings.servicesTable.deleteGroup.warningBody")}
                </Alert>
                <ControlLabel>
                  {t("searchFindings.servicesTable.deleteGroup.typeGroupName")}
                </ControlLabel>
              </Row>
              <Row>
                <Input
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                  validate={required}
                />
              </Row>
              <Row>
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
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.rename"
                    )}
                  </option>
                  <option value={"MIGRATION"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.migration"
                    )}
                  </option>
                  <option value={"POC_OVER"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.pocOver"
                    )}
                  </option>
                  <option value={"TR_CANCELLED"}>
                    {t(
                      "searchFindings.servicesTable.deleteGroup.reason.trCancelled"
                    )}
                  </option>
                  <option value={"OTHER"}>
                    {t("searchFindings.servicesTable.deleteGroup.reason.other")}
                  </option>
                </Select>
              </Row>
              <Row>
                <TextArea
                  label={t("searchFindings.servicesTable.modal.observations")}
                  name={"comments"}
                  placeholder={t(
                    "searchFindings.servicesTable.modal.observationsPlaceholder"
                  )}
                  validate={composeValidators([validTextField, maxLength250])}
                />
              </Row>
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
