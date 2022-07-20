import { faCheck } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FieldProps } from "formik";
import React, { Fragment } from "react";

import type { ICheckboxBoxProps } from "./styles";
import { CheckboxBox, CheckboxInput, CheckboxLabel } from "./styles";

import { Alert } from "components/Alert";
import { Text } from "components/Text";

interface ICheckboxProps extends ICheckboxBoxProps {
  id?: string;
  label: React.ReactNode;
  name: string;
  value: string;
}

const CustomCheckbox: React.FC<
  FieldProps<string, Record<string, string>> & ICheckboxProps
> = ({
  disabled,
  field,
  form,
  id,
  label,
  value,
}: Readonly<
  FieldProps<string, Record<string, string>> & ICheckboxProps
>): JSX.Element => {
  const { checked, name, onBlur, onChange } = field;
  const alert = form.errors[name];

  return (
    <Fragment>
      <CheckboxLabel htmlFor={id}>
        <CheckboxBox disabled={disabled}>
          <CheckboxInput
            aria-label={name}
            checked={checked}
            disabled={disabled}
            id={id}
            name={name}
            onBlur={onBlur}
            onChange={onChange}
            value={value}
          />
          <FontAwesomeIcon icon={faCheck} />
        </CheckboxBox>
        <Text ml={2}>{label}</Text>
      </CheckboxLabel>
      {alert === undefined ? undefined : <Alert icon={true}>{alert}</Alert>}
    </Fragment>
  );
};

export type { ICheckboxProps };
export { CustomCheckbox };
