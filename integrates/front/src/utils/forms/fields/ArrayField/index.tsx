import { ArrayWrapper } from "./wrapper";
import { FieldArray } from "redux-form";
import React from "react";

interface IArrayProps {
  children: (fieldName: string) => React.ReactNode;
  name: string;
}

const ArrayField: React.FC<IArrayProps> = ({
  children,
  name,
}: IArrayProps): JSX.Element => {
  return (
    <FieldArray component={ArrayWrapper} name={name}>
      {children}
    </FieldArray>
  );
};

export { ArrayField };
