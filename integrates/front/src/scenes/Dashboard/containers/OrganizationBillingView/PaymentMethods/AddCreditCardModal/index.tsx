import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { boolean, object, string } from "yup";

import { Button } from "components/Button";
import { Checkbox } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IAddCreditCardModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardCvc: string;
    cardExpirationMonth: string;
    cardExpirationYear: string;
    cardNumber: string;
    makeDefault: boolean;
  }) => Promise<void>;
  onChangeMethod: React.Dispatch<
    React.SetStateAction<"CREDIT_CARD" | "OTHER_METHOD" | false>
  >;
}

const validations = object().shape({
  cardCvc: string().required(),
  cardExpirationMonth: string().required(),
  cardExpirationYear: string().required(),
  cardNumber: string().required(),
  makeDefault: boolean(),
});

export const AddCreditCardModal: React.FC<IAddCreditCardModalProps> = ({
  onClose,
  onSubmit,
  onChangeMethod,
}: IAddCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  function goToOtherMethods(): void {
    onChangeMethod("OTHER_METHOD");
  }

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.creditCard.add")}
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
                {t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.cvc"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"cardCvc"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.expirationMonth"
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
                  "organization.tabs.billing.paymentMethods.add.creditCard.expirationYear"
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
                {t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.number"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"cardNumber"} type={"text"} />
            </div>
            <div>
              <Checkbox
                label={t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.default"
                )}
                name={"makeDefault"}
              />
            </div>
            <ModalConfirm
              disabled={!dirty || isSubmitting}
              onCancel={onClose}
            />
            <hr />
            <div>
              <Button
                id={"other-payment-methods"}
                onClick={goToOtherMethods}
                type={"button"}
              >
                {t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.otherPaymentMethod"
                )}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
