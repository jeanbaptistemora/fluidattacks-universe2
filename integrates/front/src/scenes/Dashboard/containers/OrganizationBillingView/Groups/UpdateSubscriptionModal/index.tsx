/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import type { IPaymentMethodAttr } from "scenes/Dashboard/containers/OrganizationBillingView/types";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";

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
        {({ dirty, isSubmitting }): JSX.Element => (
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
              <Field component={FormikDropdown} name={"paymentId"}>
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
              </Field>
            </div>
            <div className={"pt2"}>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.groups.updateSubscription.subscription"
                )}
              </ControlLabel>
              <Field
                component={FormikDropdown}
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
              </Field>
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
