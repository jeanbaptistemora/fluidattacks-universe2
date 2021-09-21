import type { FieldProps, FormikHandlers } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { StyledInput, ValidationError } from "utils/forms/fields/styles";

interface ITextProps extends FieldProps<string, Record<string, string>> {
  disabled: boolean;
  id: string;
  max: number | string;
  min: number | string;
  placeholder: string;
  type: string;
  customBlur: FormikHandlers["handleBlur"] | undefined;
}

export const FormikText: React.FC<ITextProps> = (
  props: ITextProps
): JSX.Element => {
  const { customBlur, disabled, field, id, max, min, placeholder, type } =
    props;
  const { name, onBlur, onChange, value } = field;

  function handleBlur(event: unknown): void {
    onBlur(event);

    if (customBlur !== undefined) {
      customBlur(event);
    }
  }

  return (
    <React.Fragment>
      <StyledInput
        autoComplete={"off"}
        disabled={disabled}
        id={id}
        max={max}
        min={min}
        name={name}
        onBlur={handleBlur}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
        value={value}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
