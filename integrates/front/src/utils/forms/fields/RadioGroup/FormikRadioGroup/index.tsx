/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
 */
import type { FieldProps } from "formik";
import { ErrorMessage } from "formik";
import React, { useCallback } from "react";

import type { IRadioGroupProps } from "components/RadioGroup";
import { RadioGroup } from "components/RadioGroup/index";
import { ValidationError } from "utils/forms/fields/styles";

interface IRadioGroupFieldProps extends FieldProps {
  children: React.ReactNode;
  label: string;
  uncheck: ((checked: boolean) => void) | null;
}

declare type FormikRadioGroupProps = IRadioGroupFieldProps & IRadioGroupProps;

export const FormikRadioGroup: React.FC<FormikRadioGroupProps> = (
  props: Readonly<FormikRadioGroupProps>
): JSX.Element => {
  const {
    field,
    form,
    children,
    initialState,
    labels,
    onSelect,
    uncheck = null,
  } = props;
  const { name } = field;

  const handleChange = useCallback(
    (value: unknown): void => {
      form.setFieldValue(name, value);
      if (uncheck) {
        uncheck(false);
      }
    },
    [form, name, uncheck]
  );

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
