import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { FormikSelect } from "components/Input/Formik/FormikSelect";
import { Modal } from "components/Modal";

interface IAddMethodPaymentProps {
  onClose: () => void;
}

export const AddPaymentMethod: React.FC<IAddMethodPaymentProps> = ({
  onClose,
}: IAddMethodPaymentProps): JSX.Element => {
  const { t } = useTranslation();

  const [paymentType, setPaymentType] = useState("");

  return (
    <Modal
      maxWidth={"420px"}
      onClose={onClose}
      open={true}
      title={t("organization.tabs.billing.paymentMethods.add.title")}
    >
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
        <option value={"CREDIT_CARD"}>{"Credit or Debit card"}</option>
        <option value={"OTHER"}>{"Other"}</option>
      </FormikSelect>
      {paymentType === "" ? undefined : (
        <div>
          {paymentType === "CREDIT_CARD" ? (
            <p>{"Credit Card selected"}</p>
          ) : (
            <p>{"Other selected"}</p>
          )}
        </div>
      )}
    </Modal>
  );
};
