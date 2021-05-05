import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";
import Datetime from "react-datetime";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

export const FormikDateTime: React.FC<FieldProps> = (
  props: FieldProps
): JSX.Element => {
  const { field } = props;
  const { name } = field;

  return (
    <React.Fragment>
      <Datetime
        inputProps={{ className: style["form-control"] }}
        utc={false}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...field}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
