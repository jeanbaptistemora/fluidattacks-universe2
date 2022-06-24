import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { boolean, object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikCheckbox, FormikText } from "utils/forms/fields";

interface IAddPaymentModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardCvc: string;
    cardExpirationMonth: string;
    cardExpirationYear: string;
    cardNumber: string;
    makeDefault: boolean;
  }) => Promise<void>;
}

const validations = object().shape({
  cardCvc: string().required(),
  cardExpirationMonth: string().required(),
  cardExpirationYear: string().required(),
  cardNumber: string().required(),
  makeDefault: boolean(),
});

export const AddPaymentModal: React.FC<IAddPaymentModalProps> = ({
  onClose,
  onSubmit,
}: IAddPaymentModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.modal.add")}
    >
      <Formik
        initialValues={{
          cardCvc: "",
          cardExpirationMonth: "",
          cardExpirationYear: "",
          cardNumber: "",
          makeDefault: false,
        }}
        name={"addPaymentMethod"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("organization.tabs.billing.paymentMethods.add.modal.cvc")}
              </ControlLabel>
              <Field component={FormikText} name={"cardCvc"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.modal.expirationMonth"
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
                  "organization.tabs.billing.paymentMethods.add.modal.expirationYear"
                )}
              </ControlLabel>
              <Field
                component={FormikText}
                name={"cardExpirationYear"}
                type={"text"}
              />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("organization.tabs.billing.paymentMethods.add.modal.number")}
              </ControlLabel>
              <Field component={FormikText} name={"cardNumber"} type={"text"} />
            </div>
            <div>
              <Field
                component={FormikCheckbox}
                label={t(
                  "organization.tabs.billing.paymentMethods.add.modal.default"
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
