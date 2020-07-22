/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap.
*/
import React from "react";
import _ from "lodash";
import { default as style } from "../../index.css";
import { FormControl, FormControlProps, HelpBlock } from "react-bootstrap";
import { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IDateProps extends WrappedFieldProps, FormControlProps {
  input: { value: string } & Omit<WrappedFieldInputProps, "value">;
}

export const Date: React.FC<IDateProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IDateProps>
): JSX.Element => {
  const { disabled, id, input, meta } = props;
  const { onBlur, onChange, value } = input;
  const { touched, error } = meta;

  return (
    <React.Fragment>
      <FormControl
        className={style.formControl}
        disabled={disabled}
        id={id}
        onBlur={onBlur}
        onChange={onChange}
        type={"date"}
        value={value.split(" ")[0]}
      />
      {touched && !_.isUndefined(error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
