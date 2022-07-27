import type { FieldProps } from "formik";
import _ from "lodash";
import type { FC, FocusEvent, KeyboardEvent, ReactNode } from "react";
import React from "react";

import type { ILabelProps } from "./Label";
import { Label } from "./Label";
import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";

type TFieldProps = FieldProps<string, Record<string, string>>;

interface IInputBase<T = HTMLElement>
  extends IStyledInputProps,
    Omit<ILabelProps, "children" | "htmlFor"> {
  disabled?: boolean;
  id?: string;
  label?: ILabelProps["children"];
  name: string;
  onBlur?: (event: FocusEvent<T>) => void;
  onFocus?: (event: FocusEvent<T>) => void;
  onKeyDown?: (event: KeyboardEvent<T>) => void;
}

interface IInputBaseProps extends IInputBase {
  children?: ReactNode;
  form: TFieldProps["form"];
}

const InputBase: FC<IInputBaseProps> = ({
  children,
  form: { errors, touched },
  id,
  label,
  name,
  required,
  tooltip,
  variant = "solid",
}: Readonly<IInputBaseProps>): JSX.Element => {
  const alert = _.get(touched, name) ?? false ? _.get(errors, name) : undefined;

  return (
    <InputBox showAlert={alert !== undefined}>
      {label === undefined ? undefined : (
        <Label htmlFor={id ?? name} required={required} tooltip={tooltip}>
          {label}
        </Label>
      )}
      <InputWrapper variant={variant}>{children}</InputWrapper>
      <Alert icon={true} show={alert !== undefined}>
        {alert}
      </Alert>
    </InputBox>
  );
};

export type { IInputBase, TFieldProps };
export { InputBase };
