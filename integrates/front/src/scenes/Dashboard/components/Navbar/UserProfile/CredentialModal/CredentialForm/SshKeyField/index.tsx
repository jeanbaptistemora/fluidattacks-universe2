import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import type { ISshKeyFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const SshKeyField: React.FC<ISshKeyFieldProps> = (
  props: ISshKeyFieldProps
): JSX.Element => {
  const { disabled } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        {t("profile.credentialsModal.form.sshKey.label")}
      </ControlLabel>
      <Field
        component={FormikTextArea}
        disabled={disabled}
        name={"sshKey"}
        placeholder={t("profile.credentialsModal.form.sshKey.placeholder")}
        type={"text"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { SshKeyField };
