import type { FieldProps, FormikHandlers } from "formik";
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
  const { errors, touched } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];

  function handleChange(event: unknown): void {
    onChange(event);

    if (customChange !== undefined) {
      customChange(event);
    }
  }

  return (
    <React.Fragment>
      <StyledSelect name={name} onChange={handleChange} value={value}>
        {children}
      </StyledSelect>
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};

export { FormikDropdown };
