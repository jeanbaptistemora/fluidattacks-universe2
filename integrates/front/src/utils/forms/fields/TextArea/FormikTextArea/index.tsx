/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  -------
  We need className to override default styles from react-bootstrap and props
  spreading is the best way to pass down props.
*/
import type { FieldInputProps, FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";

interface ITextAreaProps extends FieldProps {
  id?: string;
  className?: string;
  input: Omit<FieldInputProps<string>, "value"> & { value: string };
  withCount?: boolean;
  disabled?: boolean;
  rows?: number;
}

export const FormikTextArea: React.FC<ITextAreaProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITextAreaProps>
): JSX.Element => {
  const {
    className,
    disabled,
    field,
    form,
    id,
    input,
    rows,
    withCount = false,
  } = props;
  const { errors } = form;
  const error = errors[field.name];
  const { value }: { value: string } = field;

  return (
    <React.Fragment>
      <textarea
        {...field}
        {...input}
        autoComplete={"off"}
        className={`${style["form-control"]} ${style["text-area"]} ${
          className === undefined ? "" : className
        }`}
        disabled={disabled}
        id={id}
        rows={rows}
        value={value}
      />
      {withCount ? (
        <div className={style.badge}>{value.length}</div>
      ) : undefined}
      {withCount && error !== undefined ? <br /> : undefined}
      <ValidationError>
        <ErrorMessage name={field.name} />
      </ValidationError>
    </React.Fragment>
  );
};
