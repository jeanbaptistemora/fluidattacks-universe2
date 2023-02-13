import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Select } from "components/Input";
import { Modal, ModalConfirm } from "components/Modal";
import type { IPaymentMethodAttr } from "scenes/Dashboard/containers/Organization-Content/OrganizationBillingView/types";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";

interface IUpdateSubscriptionProps {
  current: string;
  groupName: string;
  onClose: () => void;
  onSubmit: (values: {
    paymentId: string | null;
    subscription: string;
  }) => Promise<void>;
  paymentId: string | null;
  paymentMethods: IPaymentMethodAttr[];
  permissions: string[];
}

const validations = object().shape({
  paymentId: string().required(),
  subscription: string().required(),
});

export const UpdateSubscriptionModal: React.FC<IUpdateSubscriptionProps> = ({
  current,
  groupName,
  onClose,
  onSubmit,
  paymentId,
  paymentMethods,
  permissions,
}: IUpdateSubscriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const subs = ["FREE", "MACHINE", "SQUAD"];
  const initialValue = subs.includes(current) ? current : "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.groups.updateSubscription.title")}
    >
      <Formik
        initialValues={{
          groupName,
          paymentId,
          subscription: initialValue,
        }}
        name={"updateSubscription"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {(): JSX.Element => (
          <Form>
            <div className={"flex flex-wrap w-100"}>
              <ControlLabel>
                {t("organization.tabs.billing.groups.name")}
              </ControlLabel>
              <Field
                component={FormikText}
                disabled={true}
                name={"groupName"}
                value={groupName}
              />
            </div>
            <div className={"pt2"}>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t("organization.tabs.billing.groups.paymentMethod")}
              </ControlLabel>
              <Select name={"paymentId"}>
                <option value={""} />
                {paymentMethods.map(
                  (method): JSX.Element => (
                    <option key={method.id} value={method.id}>{`${
                      method.lastFourDigits === ""
                        ? `${method.country}, ${method.businessName}`
                        : `${method.brand}, ${method.lastFourDigits}`
                    }`}</option>
                  )
                )}
              </Select>
            </div>
            <div className={"pt2"}>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.groups.updateSubscription.subscription"
                )}
              </ControlLabel>
              <Select
                disabled={
                  !permissions.includes(
                    "api_mutations_update_subscription_mutate"
                  )
                }
                name={"subscription"}
              >
                <option value={""} />
                {subs.map(
                  (sub: string): JSX.Element => (
                    <option key={sub} value={sub}>
                      {t(
                        `organization.tabs.billing.groups.updateSubscription.types.${sub.toLowerCase()}`
                      )}
                    </option>
                  )
                )}
              </Select>
            </div>
            <ModalConfirm disabled={true} onCancel={onClose} />
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
