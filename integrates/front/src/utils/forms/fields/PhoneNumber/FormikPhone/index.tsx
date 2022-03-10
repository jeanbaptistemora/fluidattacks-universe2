import { ErrorMessage, useField } from "formik";
import _ from "lodash";
import React from "react";
import type { CountryData } from "react-intl-tel-input/dist/types";

import type { IPhoneData, IPhoneNumberProps } from "./types";

import {
  StyledPhoneNumberInput,
  ValidationError,
} from "utils/forms/fields/styles";

export const FormikPhone: React.FC<IPhoneNumberProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IPhoneNumberProps>
): JSX.Element => {
  const { autoFocus, disabled, field, placeholder } = props;
  const { name, value }: { name: string; value: IPhoneData | undefined } =
    field;
  const [, , helpers] = useField(name);

  function setPhoneNumber(
    currentNumber: string,
    countryData: CountryData
  ): void {
    const dialCode = _.isUndefined(countryData.dialCode)
      ? ""
      : countryData.dialCode;
    const iso2 = _.isUndefined(countryData.iso2) ? "" : countryData.iso2;
    const info = {
      callingCountryCode: dialCode,
      countryCode: iso2,
      nationalNumber: currentNumber.replace(/[\s()-]/gu, ""),
    };
    helpers.setValue(info);
  }
  function onPhoneNumberChange(
    _isValid: boolean,
    currentNumber: string,
    selectedCountryData: CountryData,
    _fullNumber: string,
    _extension: string
  ): void {
    if (disabled === true) {
      return;
    }
    setPhoneNumber(currentNumber, selectedCountryData);
  }
  function onSelectFlag(
    currentNumber: string,
    selectedCountryData: CountryData,
    _fullNumber: string,
    _isValid: boolean
  ): void {
    if (disabled === true) {
      return;
    }
    setPhoneNumber(currentNumber, selectedCountryData);
  }

  return (
    <React.Fragment>
      <StyledPhoneNumberInput
        // eslint-disable-next-line jsx-a11y/no-autofocus
        autoFocus={autoFocus}
        defaultCountry={_.get(value, "countryCode", "")}
        disabled={disabled}
        formatOnInit={true}
        onPhoneNumberChange={onPhoneNumberChange}
        onSelectFlag={onSelectFlag}
        placeholder={placeholder}
        preferredCountries={["co", "us"]}
        value={_.get(value, "nationalNumber", "")}
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
