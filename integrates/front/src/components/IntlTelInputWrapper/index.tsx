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
  const { className, telInputProps } = props;
  function onKeyDown(event: React.KeyboardEvent<HTMLInputElement>): void {
    if (event.key.length > 1 || /[\d\s()-]/u.test(event.key)) return;
    if (event.ctrlKey) return;
    event.preventDefault();
  }
  function onPaste(event: React.ClipboardEvent<HTMLInputElement>): void {
    const data: string = event.clipboardData.getData("text/plain");
    if (/^[\d\s()-]*$/u.test(data)) return;
    event.preventDefault();
  }
  const inputProps: React.InputHTMLAttributes<HTMLInputElement> = {
    ...telInputProps,
    onKeyDown,
    onPaste,
  };

  return (
    <IntlTelInput
      {...props}
      containerClassName={"intl-tel-input w-100"}
      inputClassName={className}
      telInputProps={inputProps}
    />
  );
};

export { IntlTelInputWrapper, IIntlTelInputWrapperProps };
