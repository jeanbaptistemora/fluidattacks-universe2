import { Field } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IOrganizationFieldProps } from "./types";

import type { IOrganizationAttr } from "../../types";
import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikDropdown } from "utils/forms/fields";
import { composeValidators, required } from "utils/validations";

const OrganizationField: React.FC<IOrganizationFieldProps> = (
  props: IOrganizationFieldProps
): JSX.Element => {
  const { disabled, organizations } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        {t("profile.credentialsModal.form.organization")}
      </ControlLabel>
      <Field
        component={FormikDropdown}
        disabled={disabled}
        name={"organization"}
        validate={composeValidators([required])}
      >
        <option value={""}>{""}</option>
        {organizations.map(
          (organization: IOrganizationAttr): JSX.Element => (
            <option key={organization.id} value={organization.id}>
              {_.capitalize(organization.name)}
            </option>
          )
        )}
      </Field>
    </FormGroup>
  );
};

export { OrganizationField };
