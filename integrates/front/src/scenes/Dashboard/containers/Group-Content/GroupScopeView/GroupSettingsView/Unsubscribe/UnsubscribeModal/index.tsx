import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";

import { Alert } from "components/Alert";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import { required } from "utils/validations";

interface IUnsubscribeModalProps {
  groupName: string;
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (values: { confirmation: string }) => void;
}

const UnsubscribeModal: React.FC<IUnsubscribeModalProps> = (
  props: IUnsubscribeModalProps
): JSX.Element => {
  const { groupName, isOpen, onClose, onSubmit } = props;
  const { t } = useTranslation();

  const formValidations: (values: { confirmation: string }) => {
    confirmation?: string;
  } = useCallback(
    (values: { confirmation: string }): { confirmation?: string } => {
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
    <React.StrictMode>
      <Modal
        open={isOpen}
        title={t("searchFindings.servicesTable.unsubscribe.title")}
      >
        <Formik
          enableReinitialize={true}
          initialValues={{
            confirmation: "",
          }}
          name={"unsubscribeFromGroup"}
          onSubmit={onSubmit}
          validate={formValidations}
        >
          {({ dirty, isValid, submitForm }): JSX.Element => (
            <Form id={"unsubscribeFromGroup"}>
              <ControlLabel>
                {t("searchFindings.servicesTable.unsubscribe.warningTitle")}
              </ControlLabel>
              <Alert>
                {t("searchFindings.servicesTable.unsubscribe.warningBody")}
              </Alert>
              <FormGroup>
                <ControlLabel>
                  {t("searchFindings.servicesTable.unsubscribe.typeGroupName")}
                </ControlLabel>
                <Field
                  component={FormikText}
                  name={"confirmation"}
                  placeholder={groupName.toLowerCase()}
                  type={"text"}
                  validate={required}
                />
              </FormGroup>
              <ModalConfirm
                disabled={!isValid || !dirty}
                onCancel={onClose}
                onConfirm={submitForm}
              />
            </Form>
          )}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};

export type { IUnsubscribeModalProps };
export { UnsubscribeModal };
