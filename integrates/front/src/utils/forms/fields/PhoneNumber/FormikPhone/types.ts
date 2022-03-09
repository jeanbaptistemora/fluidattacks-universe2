import type { FieldProps } from "formik";

interface IPhoneNumberProps extends FieldProps {
  autoFocus?: boolean;
  disabled?: boolean;
  placeholder?: string;
}

interface IPhoneData {
  countryDialCode: string;
  countryIso2: string;
  nationalNumber: string;
}

export { IPhoneNumberProps, IPhoneData };
