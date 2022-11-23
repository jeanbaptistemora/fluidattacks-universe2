import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { FieldArray } from "formik";
import React from "react";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";

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
                    <Col>{children(fieldName)}</Col>
                    <Col>
                      {index > 0 || allowEmpty ? (
                        <Button onClick={removeItem} variant={"secondary"}>
                          <FontAwesomeIcon icon={faTrashAlt} />
                        </Button>
                      ) : undefined}
                      {index === arrayValues.length ? (
                        <Button onClick={addItem} variant={"secondary"}>
                          <FontAwesomeIcon icon={faPlus} />
                        </Button>
                      ) : undefined}
                    </Col>
                  </Row>
                </React.Fragment>
              );
            })}
            <Row>
              <Col>
                <Button onClick={addItem} variant={"secondary"}>
                  <FontAwesomeIcon icon={faPlus} />
                </Button>
              </Col>
            </Row>
          </React.Fragment>
        );
      }}
    </FieldArray>
  );
};

export type { IArrayProps };
export { FormikArrayField };
