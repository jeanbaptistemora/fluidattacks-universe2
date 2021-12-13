import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikTextArea } from "utils/forms/fields";
import {
  composeValidators,
  maxLength,
  validTextField,
} from "utils/validations";

const MAX_COMMENTS_LENGTH: number = 200;
const maxCommentsLength: ConfigurableValidator = maxLength(MAX_COMMENTS_LENGTH);
const CommentsField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.editModal.fields.comments")}</b>
      </ControlLabel>
      <Field
        component={FormikTextArea}
        name={"comments"}
        type={"text"}
        validate={composeValidators([validTextField, maxCommentsLength])}
      />
    </FormGroup>
  );
};

export { CommentsField };
