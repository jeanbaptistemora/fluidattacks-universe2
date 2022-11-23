import _ from "lodash";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { Input } from "components/Input";
import { composeValidators, required } from "utils/validations";

interface IVerifyCodeFieldProps {
  disabled?: boolean;
  name?: string;
}

const VerifyCodeField: FC<IVerifyCodeFieldProps> = ({
  disabled,
  name,
}: Readonly<IVerifyCodeFieldProps>): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Input
      disabled={disabled}
      label={t("profile.mobileModal.fields.verificationCode")}
      name={_.isUndefined(name) ? "verificationCode" : name}
      validate={composeValidators([required])}
    />
  );
};

export { VerifyCodeField };
