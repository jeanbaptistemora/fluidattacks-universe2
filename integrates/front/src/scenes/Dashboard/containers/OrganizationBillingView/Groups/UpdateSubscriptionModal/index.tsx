import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikDropdown, FormikText } from "utils/forms/fields";

interface IUpdateSubscriptionProps {
  current: string;
  groupName: string;
  managed: boolean;
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
      size={"small"}
      title={t("organization.tabs.billing.groups.updateSubscription.title")}
    >
      <Formik
        initialValues={{
          groupName,
          managed: String(managed),
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
                <option value={"true"}>
                  {t("organization.tabs.billing.groups.managed.yes")}
                </option>
                <option value={"false"}>
                  {t("organization.tabs.billing.groups.managed.no")}
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
            <div className={"pt2"}>
              <ModalFooter>
                <Button onClick={onClose} variant={"secondary"}>
                  {t("confirmmodal.cancel")}
                </Button>
                <Button
                  disabled={!dirty || isSubmitting}
                  type={"submit"}
                  variant={"primary"}
                >
                  {t("confirmmodal.proceed")}
                </Button>
              </ModalFooter>
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
