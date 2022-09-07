/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FieldArray } from "formik";
import type { FC, ReactNode } from "react";
import React, { Fragment } from "react";

import type { IInputProps } from "./FormikInput";

import { Input } from "../Fields/Input";
import { Label } from "../Label";
import { Button } from "components/Button";
import { Gap } from "components/Layout";

interface IInputArrayProps
  extends Omit<IInputProps, "childLeft" | "childRight" | "type"> {
  initValue?: string;
  max?: number;
}

const FormikArray: FC<IInputArrayProps> = ({
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
}: Readonly<IInputArrayProps>): JSX.Element => (
  <FieldArray name={name}>
    {({ form, push, remove }): ReactNode => {
      function addItem(): void {
        push(initValue);
      }

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
                function removeItem(): void {
                  remove(index);
                }

                return (
                  <Input
                    childLeft={
                      <Button
                        icon={faTrashAlt}
                        onClick={removeItem}
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
    }}
  </FieldArray>
);

export type { IInputArrayProps };
export { FormikArray };
