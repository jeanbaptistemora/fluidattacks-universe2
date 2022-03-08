import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { Button } from "components/Button";
import { Modal, ModalFooter } from "components/Modal";
import { ControlLabel, RequiredField } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";

interface IUpdateSubscriptionProps {
  groupName: string;
  current: string;
  onClose: () => void;
  onSubmit: (values: { subscription: string }) => Promise<void>;
}

const validations = object().shape({
  subscription: string().required(),
});

export const UpdateSubscriptionModal: React.FC<IUpdateSubscriptionProps> = ({
  groupName,
  current,
  onClose,
  onSubmit,
}: IUpdateSubscriptionProps): JSX.Element => {
  const { t } = useTranslation();
  const subs = ["FREE", "MACHINE", "SQUAD"];
  const initialValue = subs.includes(current) ? current : "";

  return (
    <Modal
      onClose={onClose}
      open={true}
      title={`${t(
        "organization.tabs.billing.groups.updateSubscription.title"
      )} ${groupName} subscription`}
    >
      <Formik
        initialValues={{
          subscription: initialValue,
        }}
        name={"updateSubscription"}
        onSubmit={onSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting }): JSX.Element => (
          <Form>
            <div>
              <ControlLabel>
                <RequiredField>{"*"}&nbsp;</RequiredField>
                {t(
                  "organization.tabs.billing.groups.updateSubscription.subscription"
                )}
              </ControlLabel>
              <Field component={FormikDropdown} name={"subscription"}>
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
            <div>
              <div>
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
            </div>
          </Form>
        )}
      </Formik>
    </Modal>
  );
};
