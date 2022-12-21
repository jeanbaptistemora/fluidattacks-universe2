import { Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { boolean, object, string } from "yup";

import { Checkbox, Input } from "components/Input";
import { Col, Row } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { composeValidators, required, validTextField } from "utils/validations";

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
    rutList: FileList | undefined;
    state: string;
    taxIdList: FileList | undefined;
  }) => Promise<void>;
}

export const UpdateCreditCardModal: React.FC<IUpdateCreditCardModalProps> = ({
  onClose,
  onSubmit,
}: IUpdateCreditCardModalProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    businessName: string(),
    cardExpirationMonth: string().required(t("validations.required")),
    cardExpirationYear: string().required(t("validations.required")),
    city: string(),
    country: string(),
    email: string(),
    makeDefault: boolean().required(),
    state: string(),
  });

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
          rutList: undefined,
          state: "",
          taxIdList: undefined,
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
                  type={"text"}
                  validate={composeValidators([required, validTextField])}
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
                  type={"text"}
                  validate={composeValidators([required, validTextField])}
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
