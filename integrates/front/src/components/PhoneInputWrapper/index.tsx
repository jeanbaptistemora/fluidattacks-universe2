/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable react/jsx-props-no-spreading */
/* eslint-disable fp/no-rest-parameters */
import React from "react";
import PhoneInput from "react-phone-input-2";
import type { PhoneInputProps } from "react-phone-input-2";

import "react-phone-input-2/lib/bootstrap.css";

interface IPhoneInputWrapperProps extends PhoneInputProps {
  className?: string;
}

const PhoneInputWrapper: React.FC<IPhoneInputWrapperProps> = (
  props: Readonly<IPhoneInputWrapperProps>
): JSX.Element => {
  const { className, ...otherProps } = props;

  return (
    <PhoneInput
      {...otherProps}
      containerClass={"w-100"}
      inputClass={className}
    />
  );
};

export { PhoneInputWrapper };
