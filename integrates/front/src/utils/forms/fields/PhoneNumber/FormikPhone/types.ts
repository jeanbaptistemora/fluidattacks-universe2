import type { FieldProps } from "formik";

interface IPhoneNumberProps extends FieldProps {
  autoFocus?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

interface IPhoneData {
  callingCountryCode: string;
  countryCode: string;
  nationalNumber: string;
}

export { IPhoneNumberProps, IPhoneData };
