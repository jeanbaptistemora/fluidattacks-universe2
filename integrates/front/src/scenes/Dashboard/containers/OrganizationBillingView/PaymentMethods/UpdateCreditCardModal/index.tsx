import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { boolean, object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikCheckbox, FormikText } from "utils/forms/fields";

interface IUpdateCreditCardModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardExpirationMonth: string;
    cardExpirationYear: string;
    makeDefault: boolean;
    businessName: string;
    city: string;
    country: string;
    email: string;
    state: string;
  }) => Promise<void>;
}

const validations = object().shape({
  businessName: string(),
  cardExpirationMonth: string().required(),
  cardExpirationYear: string().required(),
  city: string(),
  country: string(),
  email: string(),
  makeDefault: boolean().required(),
  state: string(),
});

export const UpdateCreditCardModal: React.FC<IUpdateCreditCardModalProps> = ({
  onClose,
  onSubmit,
}: IUpdateCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.update.modal.update")}
    >
      <Formik
        initialValues={{
          businessName: "",
          cardExpirationMonth: "",
          cardExpirationYear: "",
          city: "",
          country: "",
          email: "",
          makeDefault: false,
          state: "",
        }}
        name={"updateCreditCard"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.update.modal.expirationMonth"
                )}
              </ControlLabel>
              <Field
                component={FormikText}
                name={"cardExpirationMonth"}
                type={"text"}
              />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.update.modal.expirationYear"
                )}
              </ControlLabel>
              <Field
                component={FormikText}
                name={"cardExpirationYear"}
                type={"text"}
              />
            </div>
            <div>
              <Field
                component={FormikCheckbox}
                label={t(
                  "organization.tabs.billing.paymentMethods.update.modal.default"
                )}
                name={"makeDefault"}
                type={"checkbox"}
              />
            </div>
            <ModalConfirm
              disabled={!dirty || isSubmitting}
              onCancel={onClose}
            />
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
