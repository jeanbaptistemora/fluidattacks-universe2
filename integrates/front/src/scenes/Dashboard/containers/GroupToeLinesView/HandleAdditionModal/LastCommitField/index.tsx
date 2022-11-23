import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  required,
  validCommitHash,
} from "utils/validations";

const LastCommitField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.addModal.fields.lastCommit")} </b>
      </ControlLabel>
      <Field
        component={FormikText}
        name={"lastCommit"}
        type={"text"}
        validate={composeValidators([required, validCommitHash])}
      />
    </FormGroup>
  );
};

export { LastCommitField };
