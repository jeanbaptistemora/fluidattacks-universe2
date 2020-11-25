import { ArrayWrapper } from "./wrapper";
import { FieldArray } from "redux-form";
import React from "react";

interface IArrayProps {
  children: (fieldName: string) => React.ReactNode;
  initialValue: unknown;
  name: string;
}

const ArrayField: React.FC<IArrayProps> = ({
  children,
  initialValue,
  name,
}: IArrayProps): JSX.Element => {
  return (
    <FieldArray
      component={ArrayWrapper}
      initialValue={initialValue}
      name={name}
    >
      {children}
    </FieldArray>
  );
};

export { ArrayField };
