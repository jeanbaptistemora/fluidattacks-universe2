import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IUpdatePaymentModalProps {
  onClose: () => void;
  onSubmit: (values: {
    cardExpirationMonth: string;
    cardExpirationYear: string;
  }) => Promise<void>;
}

const validations = object().shape({
  cardExpirationMonth: string().required(),
  cardExpirationYear: string().required(),
});

export const UpdatePaymentModal: React.FC<IUpdatePaymentModalProps> = ({
  onClose,
  onSubmit,
}: IUpdatePaymentModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal
      headerTitle={t(
        "organization.tabs.billing.paymentMethods.update.modal.update"
      )}
      onEsc={onClose}
      open={true}
    >
      <Formik
        initialValues={{
          cardExpirationMonth: "",
          cardExpirationYear: "",
        }}
        name={"updatePaymentMethod"}
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
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose}>{t("confirmmodal.cancel")}</Button>
                  <Button disabled={!dirty || isSubmitting} type={"submit"}>
                    {t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
