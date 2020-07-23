import { default as Datetime } from "react-datetime";
import React from "react";
import { WrappedFieldProps } from "redux-form";
import _ from "lodash";
import { default as style } from "../../index.css";
import { FormControlProps, HelpBlock } from "react-bootstrap";
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
        inputProps={{ className: style.formControl }}
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
