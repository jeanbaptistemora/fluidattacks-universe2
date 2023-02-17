import { FieldArray } from "formik";
import React from "react";

import { ActionButtons } from "./ActionButtons";

interface IArrayProps {
  allowEmpty: boolean;
  children: (fieldName: string) => React.ReactNode;
  initialValue: unknown;
  name: string;
}

const FormikArrayField: React.FC<IArrayProps> = ({
  allowEmpty,
  children,
  initialValue,
  name,
}: IArrayProps): JSX.Element => {
  return (
    <FieldArray name={name}>
      {({ form, push, remove }): React.ReactNode => {
        return (
          <ActionButtons
            allowEmpty={allowEmpty}
            form={form}
            initialValue={initialValue}
            name={name}
            push={push}
            remove={remove}
          >
            {children}
          </ActionButtons>
        );
      }}
    </FieldArray>
  );
};

export type { IArrayProps };
export { FormikArrayField };
