import _ from "lodash";
import React from "react";
import Datetime from "react-datetime";
import type { WrappedFieldProps } from "redux-form";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

export const DateTime: React.FC<WrappedFieldProps> = (
  props: WrappedFieldProps
): JSX.Element => {
  const { input, meta } = props;
  const { touched, error } = meta;

  return (
    <React.Fragment>
      <Datetime
        inputProps={{ className: style["form-control"] }}
        utc={false}
        // Best way to pass down props.
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...input}
      />
      {touched && !_.isUndefined(error) && (
        <ValidationError id={"validationError"}>
          {error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};
