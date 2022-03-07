import type { FieldProps } from "formik";
import { ErrorMessage, useField } from "formik";
import _ from "lodash";
import React from "react";
import type { CountryData } from "react-intl-tel-input/dist/types";

import {
  StyledPhoneNumberInput,
  ValidationError,
} from "utils/forms/fields/styles";

interface IPhoneNumberProps extends FieldProps {
  disabled?: boolean;
  placeholder?: string;
}

export const FormikPhoneNumber: React.FC<IPhoneNumberProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IPhoneNumberProps>
): JSX.Element => {
  const { disabled, field, placeholder } = props;
  const { name, value } = field;
  const [, , helpers] = useField(name);

  function setPhoneNumber(
    currentNumber: string,
    countryData: CountryData
  ): void {
    const dialCode = _.isUndefined(countryData.dialCode)
      ? ""
      : countryData.dialCode;
    const fullNumber = `+${dialCode}${currentNumber}`;
    helpers.setValue(fullNumber.replace(/[\s()-]/gu, ""));
  }
  function onPhoneNumberChange(
    _isValid: boolean,
    currentNumber: string,
    selectedCountryData: CountryData,
    _fullNumber: string,
    _extension: string
  ): void {
    setPhoneNumber(currentNumber, selectedCountryData);
  }
  function onSelectFlag(
    currentNumber: string,
    selectedCountryData: CountryData,
    _fullNumber: string,
    _isValid: boolean
  ): void {
    setPhoneNumber(currentNumber, selectedCountryData);
  }

  return (
    <React.Fragment>
      <StyledPhoneNumberInput
        defaultValue={value}
        disabled={disabled}
        formatOnInit={true}
        onPhoneNumberChange={onPhoneNumberChange}
        onSelectFlag={onSelectFlag}
        placeholder={placeholder}
        preferredCountries={["co", "us"]}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
