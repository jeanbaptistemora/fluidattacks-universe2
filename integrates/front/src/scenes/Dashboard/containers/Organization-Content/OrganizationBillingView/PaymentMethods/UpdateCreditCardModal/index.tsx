import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { boolean, number, object } from "yup";

import { Checkbox, Input } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";

interface IUpdateCreditCardModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardExpirationMonth: number | undefined;
    cardExpirationYear: number | undefined;
    makeDefault: boolean;
  }) => Promise<void>;
}

export const UpdateCreditCardModal: React.FC<IUpdateCreditCardModalProps> = ({
  onClose,
  onSubmit,
}: IUpdateCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    cardExpirationMonth: number()
      .integer(t("validations.integer"))
      .positive(t("validations.positive"))
      .required(t("validations.required")),
    cardExpirationYear: number()
      .integer(t("validations.integer"))
      .positive(t("validations.positive"))
      .required(t("validations.required")),
    makeDefault: boolean().required(),
  });

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.update.modal.update")}
    >
      <Formik
        initialValues={{
          cardExpirationMonth: undefined,
          cardExpirationYear: undefined,
          makeDefault: false,
        }}
        name={"updateCreditCard"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <Row>
              <Col lg={50}>
                <Input
                  id={"add-card-expiration-month"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationMonth.label"
                  )}
                  name={"cardExpirationMonth"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationMonth.placeholder"
                  )}
                  type={"number"}
                />
              </Col>
              <Col lg={50}>
                <Input
                  id={"add-card-expiration-year"}
                  label={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationYear.label"
                  )}
                  name={"cardExpirationYear"}
                  placeholder={t(
                    "organization.tabs.billing.paymentMethods.add.creditCard.expirationYear.placeholder"
                  )}
                  type={"number"}
                />
              </Col>
            </Row>
            <Row>
              <Checkbox
                label={t(
                  "organization.tabs.billing.paymentMethods.update.modal.default"
                )}
                name={"makeDefault"}
              />
            </Row>
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
