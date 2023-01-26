import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IVerificationCodeFieldProps } from "./types";

import { Input } from "components/Input";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { composeValidators, required } from "utils/validations";

const VerificationCodeField: React.FC<IVerificationCodeFieldProps> = (
  props: IVerificationCodeFieldProps
): JSX.Element => {
  const { disabled, name } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("profile.mobileModal.fields.verificationCode")}</b>
      </ControlLabel>
      <Input
        disabled={disabled}
        name={_.isUndefined(name) ? "verificationCode" : name}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { VerificationCodeField };
