import type { FieldProps } from "formik";
import React from "react";
import PhoneInput from "react-phone-input-2";

import style from "utils/forms/index.css";
import "react-phone-input-2/lib/bootstrap.css";

export const FormikPhoneNumber: React.FC<FieldProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: FieldProps
): JSX.Element => {
  const { field } = props;
  const { onChange, value: phoneFormValue } = field;

  function handlePhoneChange(value: string): void {
    onChange(`+${value}`);
  }

  return (
    <PhoneInput
      country={"co"}
      inputClass={style["form-control"]}
      masks={{ co: "(...) ... ...." }}
      onChange={handlePhoneChange}
      value={phoneFormValue}
    />
  );
};
