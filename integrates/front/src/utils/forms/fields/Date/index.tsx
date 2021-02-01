/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap.
*/
import React from "react";
import _ from "lodash";
import style from "utils/forms/index.css";
import type { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface IDateProps extends WrappedFieldProps {
  className?: string;
  disabled?: boolean;
  id?: string;
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
      <input
        className={style["form-control"]}
        disabled={disabled}
        id={id}
        onBlur={onBlur}
        onChange={onChange}
        type={"date"}
        value={value.split(" ")[0]}
      />
      {touched && !_.isUndefined(error) && (
        <div className={style.validationError} id={"validationError"}>
          {error as string}
        </div>
      )}
    </React.Fragment>
  );
};
