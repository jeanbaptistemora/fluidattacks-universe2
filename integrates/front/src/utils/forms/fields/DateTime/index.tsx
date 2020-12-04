import Datetime from "react-datetime";
import type { FormControlProps } from "react-bootstrap";
import { HelpBlock } from "react-bootstrap";
import React from "react";
import type { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import style from "utils/forms/index.css";
import "react-datetime/css/react-datetime.css";

export const DateTime: React.FC<WrappedFieldProps & FormControlProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: WrappedFieldProps & FormControlProps
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
        <HelpBlock
          // We need it to override default styles from react-bootstrap.
          // eslint-disable-next-line react/forbid-component-props
          className={style.validationError}
          id={"validationError"}
        >
          {error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
