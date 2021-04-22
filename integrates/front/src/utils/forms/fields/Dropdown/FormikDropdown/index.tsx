import type { FieldProps } from "formik";
import React from "react";
import styled from "styled-components";

import { ValidationError } from "styles/styledComponents";

const StyledSelect = styled.select.attrs({
  className: "w-100 pa2 gray bg-white bw1 b--light-gray",
})``;

interface IDropdownProps extends FieldProps<string, Record<string, string>> {
  children: React.ReactNode;
}

const FormikDropdown: React.FC<IDropdownProps> = ({
  children,
  field,
  form,
}: IDropdownProps): JSX.Element => {
  const { name, onChange } = field;
  const { errors, initialValues, touched } = form;
  const initialValue = initialValues[name];
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];

  return (
    <React.Fragment>
      <StyledSelect defaultValue={initialValue} name={name} onChange={onChange}>
        {children}
      </StyledSelect>
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};

export { FormikDropdown };
