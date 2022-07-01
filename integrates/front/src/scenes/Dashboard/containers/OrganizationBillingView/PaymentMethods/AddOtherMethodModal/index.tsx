import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IAddOtherMethodModalProps {
  onClose: () => void;
  onSubmit: (values: {
    businessName: string;
    city: string;
    country: string;
    email: string;
    rut: string;
    taxId: string;
  }) => void;
  onChangeMethod: React.Dispatch<
    React.SetStateAction<"CREDIT_CARD" | "OTHER_METHOD" | false>
  >;
}

const validations = object().shape({
  businessName: string().required(),
  city: string().required(),
  country: string().required(),
  email: string().required(),
  rut: string().required(),
  taxId: string().required(),
});

export const AddOtherMethodModal: React.FC<IAddOtherMethodModalProps> = ({
  onClose,
  onSubmit,
  onChangeMethod,
}: IAddOtherMethodModalProps): JSX.Element => {
  const { t } = useTranslation();

  function goToCreditCard(): void {
    onChangeMethod("CREDIT_CARD");
  }

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.otherMethods.add")}
    >
      <Formik
        initialValues={{
          businessName: "",
          city: "",
          country: "",
          email: "",
          rut: "",
          taxId: "",
        }}
        name={"addOtherMethods"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.businessName"
                )}
              </ControlLabel>
              <Field
                component={FormikText}
                name={"businessName"}
                type={"text"}
              />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.country"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"country"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.email"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"email"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.rut"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"rut"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.taxId"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"taxId"} type={"text"} />
            </div>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.city"
                )}
              </ControlLabel>
              <Field component={FormikText} name={"city"} type={"text"} />
            </div>
            <ModalConfirm
              disabled={!dirty || isSubmitting}
              onCancel={onClose}
            />
            <hr />
            <div>
              <Button
                id={"other-payment-methods"}
                onClick={goToCreditCard}
                type={"button"}
              >
                {t(
                  "organization.tabs.billing.paymentMethods.add.otherMethods.creditCard"
                )}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
