import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import type { IActionButtonsProps } from "utils/forms/fields/ArrayField/FormikArrayField/ActionButtons";

export const ActionButtons: React.FC<IActionButtonsProps> = ({
  allowEmpty,
  children,
  form,
  initialValue,
  name,
  push,
  remove,
}: IActionButtonsProps): JSX.Element => {
  const addItem = useCallback((): void => {
    push(initialValue);
  }, [initialValue, push]);

  const removeItem = useCallback(
    (index: number): (() => void) =>
      (): void => {
        remove(index);
      },
    [remove]
  );

  const arrayValues = (form.values as Record<string, unknown>)[
    name
  ] as unknown[];

  return (
    <React.Fragment>
      {arrayValues.map((_, index: number): JSX.Element => {
        const fieldName = `${name}[${index}]`;

        return (
          <React.Fragment key={fieldName + String(index)}>
            <Row>
              <Col>{children(fieldName)}</Col>
              <Col>
                {index > 0 || allowEmpty ? (
                  <Button onClick={removeItem(index)} variant={"secondary"}>
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
};
