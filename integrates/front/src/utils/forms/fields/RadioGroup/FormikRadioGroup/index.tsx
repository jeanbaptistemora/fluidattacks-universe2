import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React from "react";

import type { IRadioGroupProps } from "components/RadioGroup";
import { RadioGroup } from "components/RadioGroup/index";
import { ValidationError } from "utils/forms/fields/styles";

interface IRadioGroupFieldProps extends FieldProps {
  children: React.ReactNode;
  label: string;
}

declare type FormikRadioGroupProps = IRadioGroupFieldProps & IRadioGroupProps;

export const FormikRadioGroup: React.FC<FormikRadioGroupProps> = (
  props: FormikRadioGroupProps
): JSX.Element => {
  const { field, form, children, initialState, labels, onSelect } = props;
  const { name } = field;

  function handleChange(value: unknown): void {
    form.setFieldValue(name, value);
  }

  return (
    <React.Fragment>
      <RadioGroup
        initialState={initialState}
        labels={labels}
        onSelect={onSelect}
        selected={handleChange}
        // eslint-disable-next-line react/jsx-props-no-spreading
        {...field}
      />
      {children}
      <ValidationError>
        <ErrorMessage name={name} />
      </ValidationError>
    </React.Fragment>
  );
};
