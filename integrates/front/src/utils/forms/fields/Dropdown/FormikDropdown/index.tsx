import type { FieldProps, FormikHandlers } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import { StyledSelect, ValidationError } from "utils/forms/fields/styles";

interface IDropdownProps extends FieldProps<string, Record<string, string>> {
  children: React.ReactNode;
  customChange: FormikHandlers["handleChange"] | undefined;
}

const FormikDropdown: React.FC<IDropdownProps> = ({
  children,
  field,
  form,
  customChange,
}: IDropdownProps): JSX.Element => {
  const { name, onChange, value } = field;

  function handleChange(event: unknown): void {
    onChange(event);

    if (customChange !== undefined) {
      customChange(event);
    }
  }

  function handleBlur(): void {
    form.setFieldTouched(name, true);
  }

  return (
    <React.Fragment>
      <StyledSelect
        aria-label={name}
        name={name}
        onBlur={handleBlur}
        onChange={handleChange}
        value={value}
      >
        {children}
      </StyledSelect>
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

export { FormikDropdown };
