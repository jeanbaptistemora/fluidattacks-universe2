/* eslint-disable react/jsx-props-no-spreading */
import React from "react";
import type { IntlTelInputProps } from "react-intl-tel-input";
import IntlTelInput from "react-intl-tel-input";
import "react-intl-tel-input/dist/main.css";

interface IIntlTelInputWrapperProps extends IntlTelInputProps {
  className?: string;
}

const IntlTelInputWrapper: React.FC<IIntlTelInputWrapperProps> = (
  props: Readonly<IIntlTelInputWrapperProps>
): JSX.Element => {
  const { className } = props;

  return <IntlTelInput {...props} inputClassName={className} />;
};

export { IntlTelInputWrapper, IIntlTelInputWrapperProps };
