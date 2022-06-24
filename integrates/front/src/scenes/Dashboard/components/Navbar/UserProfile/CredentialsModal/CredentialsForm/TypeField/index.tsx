import { Field, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../types";
import { FormGroup } from "styles/styledComponents";
import { FormikRadioGroup } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const TypeField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { values } = useFormikContext<IFormValues>();

  return (
    <FormGroup>
      <Field
        component={FormikRadioGroup}
        initialState={
          _.isUndefined(values.isHttpsType)
            ? t("profile.credentialsModal.form.ssh")
            : values.isHttpsType
            ? t("profile.credentialsModal.form.https")
            : t("profile.credentialsModal.form.ssh")
        }
        labels={[
          t("profile.credentialsModal.form.https"),
          t("profile.credentialsModal.form.ssh"),
        ]}
        name={"isHttpsType"}
        type={"Radio"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { TypeField };
