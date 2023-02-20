/* eslint-disable react/require-default-props */
import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import type { FormikProps } from "formik";
import React, { Fragment, useCallback } from "react";

import type { IInputProps } from "./FormikInput";

import { Input } from "../Fields/Input";
import { Button } from "components/Button";
import { Label } from "components/Input/Label";
import { Gap } from "components/Layout";

interface IActionButtons
  extends Omit<IInputProps, "childLeft" | "childRight" | "type"> {
  initValue?: string;
  max?: number;
  form: FormikProps<unknown>;
  push: (obj: unknown) => void;
  remove: <T>(index: number) => T | undefined;
}

export const ActionButtons: React.FC<IActionButtons> = ({
  disabled,
  id,
  initValue = "",
  label,
  max = 10,
  name,
  onBlur,
  onChange,
  onFocus,
  onKeyDown,
  placeholder,
  required,
  tooltip,
  validate,
  variant,
  form,
  push,
  remove,
}: IActionButtons): JSX.Element => {
  const addItem = useCallback((): void => {
    push(initValue);
  }, [initValue, push]);

  const removeItem = useCallback(
    (index: number): (() => void) =>
      (): void => {
        remove(index);
      },
    [remove]
  );

  const values = (form.values as Record<string, unknown>)[name] as string[];

  return (
    <Gap disp={"block"} id={id} mv={8}>
      <Label htmlFor={id} required={required} tooltip={tooltip}>
        {label}
      </Label>
      {values.length > 0 ? (
        <Fragment>
          {values.map((_, index: number): JSX.Element => {
            const fieldName = `${name}[${index}]`;

            return (
              <Input
                childLeft={
                  <Button
                    icon={faTrashAlt}
                    onClick={removeItem(index)}
                    size={"sm"}
                    variant={"secondary"}
                  />
                }
                disabled={disabled}
                key={fieldName}
                name={fieldName}
                onBlur={onBlur}
                onChange={onChange}
                onFocus={onFocus}
                onKeyDown={onKeyDown}
                placeholder={placeholder}
                validate={validate}
                variant={variant}
              />
            );
          })}
        </Fragment>
      ) : undefined}
      {values.length < max ? (
        <Button icon={faPlus} onClick={addItem} variant={"secondary"} />
      ) : undefined}
    </Gap>
  );
};
