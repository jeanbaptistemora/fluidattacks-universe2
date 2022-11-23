import { Field } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import type { IPhoneFieldProps } from "./types";

import { ControlLabel, FormGroup } from "styles/styledComponents";
import { FormikPhone } from "utils/forms/fields/PhoneNumber/FormikPhone";
import {
  composeValidators,
  isValidPhoneNumber,
  required,
} from "utils/validations";

const PhoneField: React.FC<IPhoneFieldProps> = (
  props: IPhoneFieldProps
): JSX.Element => {
  const { autoFocus, disabled, label, name } = props;
  const { t } = useTranslation();

  return (
    <FormGroup>
      <ControlLabel>
        <b>
          {t(
            _.isUndefined(label)
              ? "profile.mobileModal.fields.phoneNumber"
              : label
          )}
        </b>
      </ControlLabel>
      <Field
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={autoFocus}
        component={FormikPhone}
        disabled={disabled}
        name={_.isUndefined(name) ? "phone" : name}
        validate={composeValidators([required, isValidPhoneNumber])}
      />
    </FormGroup>
  );
};

export { PhoneField };
