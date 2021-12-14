import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { FieldArray } from "formik";
import React from "react";

import { Button } from "components/Button";
import { Col80, RemoveTag, Row } from "styles/styledComponents";

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
        function addItem(): void {
          push(initialValue);
        }
        const arrayValues = (form.values as Record<string, unknown>)[
          name
        ] as unknown[];

        return (
          <React.Fragment>
            {arrayValues.map((_, index: number): JSX.Element => {
              const fieldName = `${name}[${index}]`;

              function removeItem(): void {
                remove(index);
              }

              return (
                <React.Fragment key={fieldName + String(index)}>
                  <Row>
                    <Col80>{children(fieldName)}</Col80>
                    <div>
                      {index > 0 || allowEmpty ? (
                        <RemoveTag>
                          <Button onClick={removeItem}>
                            <FontAwesomeIcon icon={faTrashAlt} />
                          </Button>
                        </RemoveTag>
                      ) : undefined}
                    </div>
                  </Row>
                  <br />
                </React.Fragment>
              );
            })}
            <br />
            <Button onClick={addItem}>
              <FontAwesomeIcon icon={faPlus} />
            </Button>
          </React.Fragment>
        );
      }}
    </FieldArray>
  );
};

export { FormikArrayField, IArrayProps };
