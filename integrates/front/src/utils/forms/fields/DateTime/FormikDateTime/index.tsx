import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import type { Moment } from "moment";
import React from "react";
import Datetime from "react-datetime";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

export const FormikDateTime: React.FC<FieldProps> = (
  props: FieldProps
): JSX.Element => {
  const { field, form } = props;
  const { name } = field;

  function handleChange(value: Moment | string): void {
    form.setFieldValue(name, value);
  }

  function handleBlur(): void {
    form.setFieldTouched(name, true);
  }

  return (
    <React.Fragment>
      <Datetime
        inputProps={{ className: style["form-control"] }}
        utc={false}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...field}
        onBlur={handleBlur}
        onChange={handleChange}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
