import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import type { Moment } from "moment";
import React from "react";
import Datetime from "react-datetime";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

interface IDateTimeProps extends FieldProps {
  disabled?: boolean;
  dataTestId?: string;
}

export const FormikDateTime: React.FC<IDateTimeProps> = (
  props: Readonly<IDateTimeProps>
): JSX.Element => {
  const { dataTestId, field, form, disabled = false } = props;
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
        inputProps={{
          className: style["form-control"],
          // @ts-expect-error It is a valid prop
          "data-testid": dataTestId,
          disabled,
          name,
        }}
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
