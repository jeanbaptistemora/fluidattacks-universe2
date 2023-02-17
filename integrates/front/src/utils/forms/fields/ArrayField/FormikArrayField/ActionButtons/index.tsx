import { faPlus, faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FormikProps } from "formik";
import React, { useCallback } from "react";

import { Button } from "components/Button";
import { Col80, RemoveTag, Row } from "styles/styledComponents";

interface IActionButtonsProps {
  allowEmpty: boolean;
  children: (fieldName: string) => React.ReactNode;
  form: FormikProps<unknown>;
  initialValue: unknown;
  name: string;
  push: (obj: unknown) => void;
  remove: <T>(index: number) => T | undefined;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
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
              <Col80>{children(fieldName)}</Col80>
              <div>
                {index > 0 || allowEmpty ? (
                  <RemoveTag>
                    <Button onClick={removeItem(index)} variant={"secondary"}>
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
      <Button onClick={addItem} variant={"secondary"}>
        <FontAwesomeIcon icon={faPlus} />
      </Button>
    </React.Fragment>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
