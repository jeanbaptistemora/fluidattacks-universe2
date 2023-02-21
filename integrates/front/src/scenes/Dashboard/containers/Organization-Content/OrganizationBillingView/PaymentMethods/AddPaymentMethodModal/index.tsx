import { useMutation } from "@apollo/client";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import { default as mixpanel } from "mixpanel-browser";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddCreditCardModal } from "./AddCreditCard";
import { ADD_CREDIT_CARD_PAYMENT_METHOD } from "./queries";

import { FormikSelect } from "components/Input/Formik/FormikSelect";
import { Row as Container } from "components/Layout";
import { Modal } from "components/Modal";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IAddMethodPaymentProps {
  organizationId: string;
  onClose: () => void;
  onUpdate: () => void;
}

export const AddPaymentMethod: React.FC<IAddMethodPaymentProps> = ({
  organizationId,
  onClose,
  onUpdate,
}: IAddMethodPaymentProps): JSX.Element => {
  const { t } = useTranslation();

  const [paymentType, setPaymentType] = useState("");
  const [addCreditCardPaymentMethod] = useMutation(
    ADD_CREDIT_CARD_PAYMENT_METHOD,
    {
      onCompleted: (): void => {
        onUpdate();
        onClose();
        msgSuccess(
          t("organization.tabs.billing.paymentMethods.add.success.body"),
          t("organization.tabs.billing.paymentMethods.add.success.title")
        );
      },
      onError: ({ graphQLErrors }): void => {
        graphQLErrors.forEach((error): void => {
          if (
            error.message ===
            "Exception - Provided payment method could not be created"
          ) {
            msgError(
              t(
                "organization.tabs.billing.paymentMethods.add.errors.couldNotBeCreated"
              )
            );
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't create payment method", error);
          }
        });
      },
    }
  );

  const handleAddCreditCardMethodSubmit = useCallback(
    async ({
      cardCvc,
      cardExpirationMonth,
      cardExpirationYear,
      cardNumber,
      makeDefault,
    }: {
      cardCvc: string;
      cardExpirationMonth: string;
      cardExpirationYear: string;
      cardNumber: string;
      makeDefault: boolean;
    }): Promise<void> => {
      mixpanel.track("AddPaymentMethod", { method: "TC" });
      await addCreditCardPaymentMethod({
        variables: {
          cardCvc,
          cardExpirationMonth,
          cardExpirationYear,
          cardNumber,
          makeDefault,
          organizationId,
        },
      });
    },
    [addCreditCardPaymentMethod, organizationId]
  );

  return (
    <Modal
      maxWidth={"420px"}
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.title")}
    >
      <Container>
        <FormikSelect
          field={{
            name: "paymentType",
            onBlur: (): void => undefined,
            onChange: (event: React.ChangeEvent<HTMLInputElement>): void => {
              const { value } = event.target;
              setPaymentType(value);
            },
            value: paymentType,
          }}
          form={{ errors: {}, touched: {} }}
          label={t("organization.tabs.billing.paymentMethods.add.label")}
          name={"paymentType"}
        >
          <option value={""}>{""}</option>
          <option value={"CREDIT_CARD"}>
            {t(
              "organization.tabs.billing.paymentMethods.add.paymentType.creditCard"
            )}
          </option>
          <option value={"OTHER"}>
            {t(
              "organization.tabs.billing.paymentMethods.add.paymentType.otherMethod"
            )}
          </option>
        </FormikSelect>
      </Container>
      {paymentType === "" ? undefined : (
        <Container>
          {paymentType === "CREDIT_CARD" ? (
            <AddCreditCardModal
              onClose={onClose}
              onSubmit={handleAddCreditCardMethodSubmit}
            />
          ) : (
            <p>{"Other selected"}</p>
          )}
        </Container>
      )}
    </Modal>
  );
};
