import type { FieldProps } from "formik";
import React from "react";
import styled from "styled-components";

import { ValidationError } from "styles/styledComponents";

const StyledSelect = styled.select.attrs({
  className: "w-100 pa2 lh-copy gray bg-white bw1 b--light-gray",
})`
  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;

interface IDropdownProps extends FieldProps<string, Record<string, string>> {
  children: React.ReactNode;
}

const FormikDropdown: React.FC<IDropdownProps> = ({
  children,
  field,
  form,
}: IDropdownProps): JSX.Element => {
  const { name, onChange, value } = field;
  const { errors, touched } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];

  return (
    <React.Fragment>
      <StyledSelect name={name} onChange={onChange} value={value}>
        {children}
      </StyledSelect>
      {fieldTouched && error !== undefined ? (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};

export { FormikDropdown };
