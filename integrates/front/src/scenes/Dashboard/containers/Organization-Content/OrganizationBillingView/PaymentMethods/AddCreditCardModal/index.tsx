import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";
import { boolean, number, object } from "yup";

import { Button } from "components/Button";
import { Checkbox, Input } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { composeValidators, maxLength } from "utils/validations";

const MAX_CARD_NUMBER_LENGTH = 17;
const MAX_DATE_NUMBER_LENGTH = 3;
const MAX_CVC_NUMBER_LENGTH = 5;

const maxCreditNumberLength: ConfigurableValidator = maxLength(
  MAX_CARD_NUMBER_LENGTH
);
const maxDateNumberLength: ConfigurableValidator = maxLength(
  MAX_DATE_NUMBER_LENGTH
);
const maxcvcNumberLength: ConfigurableValidator = maxLength(
  MAX_CVC_NUMBER_LENGTH
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
    cardCvc: number()
      .positive(t("validations.positive"))
      .integer(t("validations.integer"))
      .required(t("validations.required")),
    cardExpirationMonth: number()
      .positive(t("validations.positive"))
      .integer(t("validations.integer"))
      .required(t("validations.required")),
    cardExpirationYear: number()
      .positive(t("validations.positive"))
      .integer(t("validations.integer"))
      .required(t("validations.required")),
    cardNumber: number()
      .positive(t("validations.positive"))
      .integer(t("validations.integer"))
      .required(t("validations.required")),
    makeDefault: boolean(),
  });

  function goToOtherMethods(): void {
    onChangeMethod("OTHER_METHOD");
  }

  return (
    <Modal
      maxWidth={"420px"}
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
                  validate={composeValidators([maxCreditNumberLength])}
                />
              </Col>
            </Row>
            <Row>
              <Col lg={33}>
                <Input
                  id={"add-card-expiration-month"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationMonth.label"
                  )}
                  name={"cardExpirationMonth"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationMonth.placeholder"
                  )}
                  type={"text"}
                  validate={composeValidators([maxDateNumberLength])}
                />
              </Col>
              <Col lg={33}>
                <Input
                  id={"add-card-expiration-year"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationYear.label"
                  )}
                  name={"cardExpirationYear"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationYear.placeholder"
                  )}
                  type={"text"}
                  validate={composeValidators([maxDateNumberLength])}
                />
              </Col>
              <Col lg={33}>
                <Input
                  id={"add-credit-card-cvc"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.cvc.label"
                  )}
                  name={"cardCvc"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.cvc.placeholder"
                  )}
                  type={"text"}
                  validate={composeValidators([maxcvcNumberLength])}
                />
              </Col>
            </Row>
            <Row>
              <Checkbox
                label={t(
                  "organization.tabs.billing.paymentMethods.add.creditCard.default"
                )}
                name={"makeDefault"}
              />
            </Row>
            <Row align={"end"} justify={"end"}>
              <Col>
                <ModalConfirm
                  disabled={!dirty || isSubmitting}
                  onCancel={onClose}
                />
              </Col>
              <Col>
                <Button
                  id={"other-payment-methods"}
                  onClick={goToOtherMethods}
                  type={"button"}
                  variant={"tertiary"}
                >
                  {t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.otherPaymentMethod"
                  )}
                </Button>
              </Col>
            </Row>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
