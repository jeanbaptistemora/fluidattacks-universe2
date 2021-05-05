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
  customChange,
}: IDropdownProps): JSX.Element => {
  const { name, onChange, value } = field;

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
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};

export { FormikDropdown };
