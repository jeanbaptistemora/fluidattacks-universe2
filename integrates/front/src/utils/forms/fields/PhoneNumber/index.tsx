import React from "react";
import PhoneInput from "react-phone-input-2";
import type { WrappedFieldProps } from "redux-form";

import style from "utils/forms/index.css";
import "react-phone-input-2/lib/bootstrap.css";

export const PhoneNumber: React.FC<WrappedFieldProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<WrappedFieldProps>
): JSX.Element => {
  const { input } = props;
  const { onChange, value: reduxFormValue } = input;

  function handlePhoneChange(value: string): void {
    onChange(`+${value}`);
  }

  return (
    <PhoneInput
      country={"co"}
      inputClass={style["form-control"]}
      masks={{ co: "(...) ... ...." }}
      onChange={handlePhoneChange}
      value={reduxFormValue}
    />
  );
};
