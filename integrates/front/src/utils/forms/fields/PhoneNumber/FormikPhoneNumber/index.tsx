import type { FieldProps } from "formik";
import { useField } from "formik";
import React from "react";
import PhoneInput from "react-phone-input-2";

import style from "utils/forms/index.css";
import "react-phone-input-2/lib/bootstrap.css";

export const FormikPhoneNumber: React.FC<FieldProps> = (
  props: FieldProps
): JSX.Element => {
  const { field } = props;
  const { name, value: phoneFormValue } = field;
  const [, , helpers] = useField(name);

  function handlePhoneChange(value: string): void {
    helpers.setValue(`+${value}`);
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
