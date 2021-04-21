/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  -------
  We need className to override default styles from react-bootstrap and props
  spreading is the best way to pass down props.
*/
import type { FieldInputProps, FieldProps } from "formik";
import { useField } from "formik";
import _ from "lodash";
import React from "react";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface ITextAreaProps extends FieldProps {
  id?: string;
  className?: string;
  input: Omit<FieldInputProps<string>, "value"> & { value: string };
  withCount?: boolean;
}

export const FormikTextArea: React.FC<ITextAreaProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITextAreaProps>
): JSX.Element => {
  const { input, id, withCount = false, field, className } = props;
  const [, meta] = useField(field.name);
  const { value }: { value: string } = field;

  return (
    <React.Fragment>
      <textarea
        {...field}
        {...input}
        className={`${style["form-control"]} ${style["text-area"]} ${
          _.isUndefined(className) ? "" : className
        }`}
        id={id}
        value={value}
      />
      {withCount ? (
        <div className={style.badge}>{value.length}</div>
      ) : undefined}
      {withCount && !_.isUndefined(meta.error) ? <br /> : undefined}
      {meta.touched && !_.isUndefined(meta.error) ? (
        <ValidationError id={"validationError"}>{meta.error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
