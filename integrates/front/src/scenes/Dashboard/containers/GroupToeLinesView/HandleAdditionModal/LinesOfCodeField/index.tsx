import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  isOptionalInteger,
  isZeroOrPositive,
  required,
} from "utils/validations";

const LinesOfCodeField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>): void {
    if (
      event.key.length > 1 ||
      /\d/u.test(event.key) ||
      event.key === "Control" ||
      event.key.toLocaleLowerCase() === "v"
    )
      return;
    event.preventDefault();
  }

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.addModal.fields.loc")} </b>
      </ControlLabel>
      <Field
        component={FormikText}
        min={"0"}
        name={"loc"}
        onKeyDown={handleKeyDown}
        step={"1"}
        type={"number"}
        validate={composeValidators([
          required,
          isOptionalInteger,
          isZeroOrPositive,
        ])}
      />
    </FormGroup>
  );
};

export { LinesOfCodeField };
