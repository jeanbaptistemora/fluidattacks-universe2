/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap.
*/
import type { FieldInputProps, FieldProps } from "formik";
import React from "react";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface IDateProps extends FieldProps {
  className?: string;
  disabled?: boolean;
  id?: string;
  input: Omit<FieldInputProps<string>, "value"> & { value: string };
}

export const FormikDate: React.FC<IDateProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IDateProps>
): JSX.Element => {
  const { disabled, id, field, form } = props;
  const { touched, errors } = form;
  const fieldTouched = Boolean(touched[field.name]);
  const error = errors[field.name];
  const { onBlur, onChange } = field;
  const { value }: { value: string } = field;

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
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
