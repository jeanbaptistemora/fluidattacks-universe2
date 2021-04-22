import type { FieldProps, FormikHandlers } from "formik";
import React from "react";
import styled from "styled-components";

import { ValidationError } from "styles/styledComponents";

const StyledInput = styled.input.attrs({
  className: "w-100 pa2 lh-copy gray bg-white bw1 b--light-gray b--solid",
})`
  &:focus {
    border-color: #d1d1d1;
    outline: none;
  }
`;

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
  const {
    customBlur,
    disabled,
    field,
    form,
    id,
    max,
    min,
    placeholder,
    type,
  } = props;
  const { name, onBlur, onChange, value } = field;
  const { errors, touched } = form;
  const fieldTouched = Boolean(touched[name]);
  const error = errors[name];

  function handleBlur(event: unknown): void {
    onBlur(event);

    if (customBlur !== undefined) {
      customBlur(event);
    }
  }

  return (
    <React.Fragment>
      <StyledInput
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
      {fieldTouched && error !== undefined && (
        <ValidationError id={"validationError"}>{error}</ValidationError>
      )}
    </React.Fragment>
  );
};
