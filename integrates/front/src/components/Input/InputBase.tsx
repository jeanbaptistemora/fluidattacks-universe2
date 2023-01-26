import type { FieldProps } from "formik";
import _ from "lodash";
import type {
  ChangeEvent,
  ClipboardEvent,
  FC,
  FocusEvent,
  KeyboardEvent,
  ReactNode,
} from "react";
import React, { useCallback } from "react";

import type { ILabelProps } from "./Label";
import { Label } from "./Label";
import type { IStyledInputProps } from "./styles";
import { InputBox, InputWrapper } from "./styles";

import { Alert } from "components/Alert";

type TField = FieldProps<string, Record<string, string>>;

type TFieldProps = Pick<TField, "field"> & {
  form: Pick<TField["form"], "errors" | "touched">;
};

interface IInput
  extends IStyledInputProps,
    Omit<ILabelProps, "children" | "htmlFor"> {
  id?: string;
  label?: ILabelProps["children"];
  name: string;
}

interface IFormikHandlers<T = HTMLElement> {
  onBlur?: (event: FocusEvent<T>) => void;
  onChange?: (event: ChangeEvent<T>) => void;
}

interface IInputBase<T = HTMLElement> extends IInput, IFormikHandlers<T> {
  disabled?: boolean;
  onFocus?: (event: FocusEvent<T>) => void;
  onKeyDown?: (event: KeyboardEvent<T>) => void;
  onPaste?: (event: ClipboardEvent<T>) => void;
  placeholder?: string;
  validate?: (value: unknown) => string | undefined;
}

interface IInputBaseProps extends IInput {
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
      {children === undefined ? undefined : (
        <InputWrapper variant={variant}>{children}</InputWrapper>
      )}
      <Alert show={alert !== undefined}>{alert}</Alert>
    </InputBox>
  );
};

const useHandlers = <T extends HTMLElement>(
  field: IFormikHandlers<T>,
  input: IFormikHandlers<T>
): [IFormikHandlers<T>["onBlur"], IFormikHandlers<T>["onChange"]] => {
  const onBlur = useCallback(
    (ev: FocusEvent<T>): void => {
      field.onBlur?.(ev);
      input.onBlur?.(ev);
    },
    [field, input]
  );
  const onChange = useCallback(
    (ev: ChangeEvent<T>): void => {
      field.onChange?.(ev);
      input.onChange?.(ev);
    },
    [field, input]
  );

  return [onBlur, onChange];
};

export type { IInputBase, TFieldProps };
export { InputBase, useHandlers };
