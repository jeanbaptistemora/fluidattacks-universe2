import Datetime from "react-datetime";
import React from "react";
import { ValidationError } from "styles/styledComponents";
import type { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

export const DateTime: React.FC<WrappedFieldProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
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
        <ValidationError
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          id={"validationError"}
        >
          {error as string}
        </ValidationError>
      )}
    </React.Fragment>
  );
};
