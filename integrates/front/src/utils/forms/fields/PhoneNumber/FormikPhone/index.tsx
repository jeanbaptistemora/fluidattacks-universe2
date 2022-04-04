import { ErrorMessage, useField } from "formik";
import _ from "lodash";
import React from "react";
import type { CountryData } from "react-phone-input-2";

import type { IPhoneData, IPhoneNumberProps } from "./types";

import { StyledPhoneInput, ValidationError } from "utils/forms/fields/styles";

export const FormikPhone: React.FC<IPhoneNumberProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<IPhoneNumberProps>
): JSX.Element => {
  const { autoFocus, disabled, field } = props;
  const { name, value }: { name: string; value: IPhoneData | undefined } =
    field;
  const [, , helpers] = useField(name);

  function onPhoneChange(
    currentNumber: string,
    countryData: CountryData,
    _event: React.ChangeEvent<HTMLInputElement>,
    _formattedValue: string
  ): void {
    const info = {
      callingCountryCode: countryData.dialCode,
      countryCode: countryData.countryCode,
      nationalNumber: currentNumber.substring(
        _.isUndefined(countryData.dialCode) ? 0 : countryData.dialCode.length
      ),
    };
    helpers.setValue(info);
  }

  return (
    <React.Fragment>
      <StyledPhoneInput
        autoFormat={true}
        country={_.get(value, "countryCode", undefined)}
        disabled={disabled}
        inputProps={{
          autoFocus,
          name: "phone",
        }}
        onChange={onPhoneChange}
        preferredCountries={["co", "us"]}
        value={
          _.get(value, "callingCountryCode", "") +
          _.get(value, "nationalNumber", "")
        }
      />
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
