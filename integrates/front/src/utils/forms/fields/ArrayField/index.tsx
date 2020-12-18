import { ArrayWrapper } from "./wrapper";
import { FieldArray } from "redux-form";
import React from "react";

interface IArrayProps {
  allowEmpty: boolean;
  children: (fieldName: string) => React.ReactNode;
  initialValue: unknown;
  name: string;
}

const ArrayField: React.FC<IArrayProps> = ({
  allowEmpty,
  children,
  initialValue,
  name,
}: IArrayProps): JSX.Element => {
  return (
    <FieldArray
      allowEmpty={allowEmpty}
      component={ArrayWrapper}
      initialValue={initialValue}
      name={name}
    >
      {children}
    </FieldArray>
  );
};

export { ArrayField, IArrayProps };
