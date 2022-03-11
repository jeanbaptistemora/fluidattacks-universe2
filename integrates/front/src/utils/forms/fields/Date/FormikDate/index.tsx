/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap.
*/
import type { FieldInputProps, FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";

interface IDateProps extends FieldProps {
  className?: string;
  disabled?: boolean;
  dataTestId?: string;
  id?: string;
  input: Omit<FieldInputProps<string>, "value"> & { value: string };
}

export const FormikDate: React.FC<IDateProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IDateProps>
): JSX.Element => {
  const { dataTestId, disabled, id, field } = props;
  const { name, onBlur, onChange } = field;
  const { value }: { value: string | undefined } = field;

  return (
    <React.Fragment>
      <input
        className={style["form-control"]}
        data-testid={dataTestId}
        disabled={disabled}
        id={id}
        name={name}
        onBlur={onBlur}
        onChange={onChange}
        type={"date"}
        value={value === undefined ? "" : value.split(" ")[0]}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
