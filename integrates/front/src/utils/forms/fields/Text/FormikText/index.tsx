/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
/* eslint-disable react/forbid-component-props
  -------
  We need it to override default styles from react-bootstrap
*/
import type { FieldProps } from "formik";
import { useField } from "formik";
import _ from "lodash";
import React from "react";

import { ValidationError } from "styles/styledComponents";
import style from "utils/forms/index.css";

interface ITextProps extends FieldProps {
  disabled: boolean;
  id: string;
  max: number | string;
  min: number | string;
  placeholder: string;
  type: string;
  // We need this type to pass customBlur functions here
  // eslint-disable-next-line @typescript-eslint/ban-types
  customBlur: Function | undefined;
}

export const FormikText: React.FC<ITextProps> = (
  props: ITextProps
): JSX.Element => {
  const {
    customBlur,
    disabled,
    id,
    field,
    max,
    min,
    placeholder,
    type,
  } = props;
  const { name, value, onBlur, onChange } = field;
  const [, meta] = useField(name);

  function handleBlur(event: unknown): void {
    onBlur(event);

    if (_.isFunction(customBlur)) {
      customBlur(event);
    }
  }

  return (
    <React.Fragment>
      <input
        className={style["form-control"]}
        disabled={disabled}
        id={id}
        max={max}
        min={min}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
        // Needed to keep the component mounted at start
        // eslint-disable-next-line @typescript-eslint/strict-boolean-expressions
        value={value || ""}
      />
      {meta.touched && !_.isUndefined(meta.error) && (
        <ValidationError id={"validationError"}>{meta.error}</ValidationError>
      )}
    </React.Fragment>
  );
};
