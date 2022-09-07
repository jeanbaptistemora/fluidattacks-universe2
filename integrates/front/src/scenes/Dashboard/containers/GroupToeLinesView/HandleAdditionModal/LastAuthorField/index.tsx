/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { Field } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  required,
  validCsvInput,
  validEmail,
} from "utils/validations";

const LastAuthorField: React.FC = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>{t("group.toe.lines.addModal.fields.lastAuthor")} </b>
      </ControlLabel>
      <Field
        component={FormikText}
        name={"lastAuthor"}
        type={"text"}
        validate={composeValidators([required, validCsvInput, validEmail])}
      />
    </FormGroup>
  );
};

export { LastAuthorField };
