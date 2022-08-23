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

interface IInput
  extends IStyledInputProps,
    Omit<ILabelProps, "children" | "htmlFor"> {
  id?: string;
  label?: ILabelProps["children"];
  name: string;
}

interface IInputBase<T = HTMLElement> extends IInput {
  disabled?: boolean;
  onBlur?: (event: FocusEvent<T>) => void;
  onFocus?: (event: FocusEvent<T>) => void;
  onKeyDown?: (event: KeyboardEvent<T>) => void;
  validate?: (value: unknown) => string | undefined;
}

interface IInputBaseProps extends IInput {
  children?: ReactNode;
  form: Pick<TFieldProps["form"], "errors" | "touched">;
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
      {children === undefined ? undefined : (
        <InputWrapper variant={variant}>{children}</InputWrapper>
      )}
      <Alert show={alert !== undefined}>{alert}</Alert>
    </InputBox>
  );
};

export type { IInputBase, TFieldProps };
export { InputBase };
