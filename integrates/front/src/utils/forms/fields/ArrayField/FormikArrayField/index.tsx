import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { FieldArray, getIn } from "formik";
import React from "react";

import { ValidationError } from "../../styles";
import { Button } from "components/Button";

interface IArrayProps {
  allowEmpty: boolean;
  children: (fieldName: string) => React.ReactNode;
  initialValue: unknown;
  name: string;
  arrayValues: unknown[];
}

const FormikArrayField: React.FC<IArrayProps> = ({
  allowEmpty,
  children,
  initialValue,
  name,
  arrayValues,
}: IArrayProps): JSX.Element => {
  return (
    <FieldArray name={name}>
      {({ form, push, remove }): React.ReactNode => {
        function addItem(): void {
          push(initialValue);
        }

        return (
          <div>
            {arrayValues.map(
              (_, index: number): JSX.Element => {
                const fieldName = `${name}.${index}`;

                function removeItem(): void {
                  remove(index);
                }
                const fieldTouched = Boolean(getIn(form.errors, fieldName));
                const error = getIn(form.errors, fieldName);

                return (
                  <div className={"flex items-end"} key={fieldName}>
                    <div className={"w-80"}>{children(fieldName)}</div>
                    <div className={"w-20"}>
                      {index > 0 || allowEmpty ? (
                        <Button onClick={removeItem}>
                          <FontAwesomeIcon icon={faTrashAlt} />
                        </Button>
                      ) : undefined}
                    </div>
                    <br />
                    {fieldTouched && typeof error === "string" ? (
                      <ValidationError id={"validationError"}>
                        {error}
                      </ValidationError>
                    ) : undefined}
                  </div>
                );
              }
            )}
            <div className={"mt4"}>
              <Button id={`${name}-add`} onClick={addItem}>
                <FontAwesomeIcon icon={faPlus} />
              </Button>
            </div>
          </div>
        );
      }}
    </FieldArray>
  );
};

export { FormikArrayField, IArrayProps };
