import { Field, useFormikContext } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../types";
import { FormGroup } from "styles/styledComponents";
import { FormikRadioGroup } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const HttpsTypeField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { values } = useFormikContext<IFormValues>();

  return (
    <FormGroup>
      <Field
        component={FormikRadioGroup}
        initialState={
          _.isUndefined(values.isHttpsPasswordType)
            ? t("profile.credentialsModal.form.httpsType.accessToken")
            : values.isHttpsPasswordType
            ? t("profile.credentialsModal.form.httpsType.userAndPassword")
            : t("profile.credentialsModal.form.httpsType.accessToken")
        }
        labels={[
          t("profile.credentialsModal.form.httpsType.userAndPassword"),
          t("profile.credentialsModal.form.httpsType.accessToken"),
        ]}
        name={"isHttpsPasswordType"}
        type={"Radio"}
        validate={composeValidators([required])}
      />
    </FormGroup>
  );
};

export { HttpsTypeField };
