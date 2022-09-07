/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FieldProps } from "formik";
import _ from "lodash";
import React from "react";

import { Switch } from "components/Switch";

interface IFormikSwitchButtonProps extends FieldProps {
  disabled?: boolean;
  offlabel: string;
  onlabel: string;
  onChange: (checked: boolean) => void;
}

// Custom SwitchButton whose state can be managed by Formik
export const FormikSwitchButton: React.FC<IFormikSwitchButtonProps> = (
  props: Readonly<IFormikSwitchButtonProps>
): JSX.Element => {
  const { disabled, field, offlabel, onlabel, onChange } = props;
  const { checked, name } = field;
  function handleOnChange(): void {
    if (!_.isUndefined(onChange)) {
      onChange(!(checked as boolean));
    }
  }

  return (
    <Switch
      checked={checked ?? false}
      disabled={disabled}
      label={{ off: offlabel, on: onlabel }}
      name={name}
      onChange={handleOnChange}
    />
  );
};
