import type { TextFieldProps } from "@mui/material/TextField";
import TextField from "@mui/material/TextField";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import type { Dayjs } from "dayjs";
import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";

import { ValidationError } from "utils/forms/fields/styles";
import style from "utils/forms/index.css";

interface IDateTimeProps extends FieldProps {
  disabled?: boolean;
  dataTestId?: string;
}

export const FormikDateTime: React.FC<IDateTimeProps> = (
  props: Readonly<IDateTimeProps>
): JSX.Element => {
  const { dataTestId, field, form, disabled = false } = props;
  const { name } = field;

  function handleChange(value: Dayjs | null): void {
    form.setFieldValue(name, value);
  }

  function handleBlur(): void {
    form.setFieldTouched(name, true);
  }

  const textField = useCallback(
    (componentProps: TextFieldProps): JSX.Element => (
      <TextField
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...componentProps}
        // eslint-disable-next-line react/forbid-component-props
        className={style["form-control"]}
        data-testid={dataTestId}
        name={name}
        onBlur={handleBlur}
      />
    ),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [name]
  );

  return (
    <React.Fragment>
      <LocalizationProvider dateAdapter={AdapterDayjs}>
        <DateTimePicker
          // eslint-disable-next-line react/jsx-props-no-spreading
          {...field}
          disabled={disabled}
          onChange={handleChange}
          renderInput={textField}
        />
      </LocalizationProvider>
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
