import type { FieldProps, FormikHandlers } from "formik";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";

import { StyledSelect, ValidationError } from "utils/forms/fields/styles";

interface IDropdownProps extends FieldProps<string, Record<string, string>> {
  children: React.ReactNode;
  customChange: FormikHandlers["handleChange"] | undefined;
  disabled: boolean | undefined;
}

const FormikDropdown: React.FC<IDropdownProps> = ({
  children,
  disabled = false,
  field,
  form,
  customChange,
}: IDropdownProps): JSX.Element => {
  const { name, onChange, value } = field;

  const handleChange = useCallback(
    (event: unknown): void => {
      onChange(event);

      if (customChange !== undefined) {
        customChange(event);
      }
    },
    [customChange, onChange]
  );

  const handleBlur = useCallback((): void => {
    form.setFieldTouched(name, true);
  }, [form, name]);

  return (
    <React.Fragment>
      <StyledSelect
        aria-label={name}
        disabled={disabled}
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
