import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";
import { boolean, object, string } from "yup";

import { Button } from "components/Button";
import { Checkbox, Input } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_CREDITCARD_NUMBER_LENGTH = 16;
const maxCreditNumberLength: ConfigurableValidator = maxLength(
  MAX_CREDITCARD_NUMBER_LENGTH
);

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

export const AddCreditCardModal: React.FC<IAddCreditCardModalProps> = ({
  onClose,
  onSubmit,
  onChangeMethod,
}: IAddCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    cardCvc: string().required(t("validations.required")),
    cardExpirationMonth: string().required(t("validations.required")),
    cardExpirationYear: string().required(t("validations.required")),
    cardNumber: string().required(t("validations.required")),
    makeDefault: boolean(),
  });

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
            <Row>
              <Col>
                <Input
                  id={"add-credit-number"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.number.label"
                  )}
                  name={"cardNumber"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.number.placeholder"
                  )}
                  type={"text"}
                  validate={composeValidators([
                    maxCreditNumberLength,
                    required,
                    validTextField,
                  ])}
                />
              </Col>
            </Row>
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
