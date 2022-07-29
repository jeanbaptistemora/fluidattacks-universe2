import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Modal, ModalConfirm } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";

interface IUpdateSubscriptionProps {
  current: string;
  groupName: string;
  managed: string;
  onClose: () => void;
  onSubmit: (values: {
    managed: string;
    subscription: string;
  }) => Promise<void>;
  permissions: string[];
}

const validations = object().shape({
  managed: string().required(),
  subscription: string().required(),
});

export const UpdateSubscriptionModal: React.FC<IUpdateSubscriptionProps> = ({
  current,
  groupName,
  managed,
  onClose,
  onSubmit,
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
          managed,
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
                {t("organization.tabs.billing.groups.managed.title")}
              </ControlLabel>
              <Field component={FormikDropdown} name={"managed"}>
                <option value={"MANAGED"}>
                  {t("organization.tabs.billing.groups.managed.managed")}
                </option>
                <option value={"NOT_MANAGED"}>
                  {t("organization.tabs.billing.groups.managed.notManaged")}
                </option>
                <option value={"UNDER_REVIEW"}>
                  {t("organization.tabs.billing.groups.managed.underReview")}
                </option>
                <option value={"TRIAL"}>
                  {t("organization.tabs.billing.groups.managed.trial")}
                </option>
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
