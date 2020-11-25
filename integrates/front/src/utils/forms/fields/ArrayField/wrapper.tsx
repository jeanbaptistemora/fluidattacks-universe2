import { Button } from "components/Button";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import type { WrappedFieldArrayProps } from "redux-form";

const ArrayWrapper: React.FC<WrappedFieldArrayProps> = (
  props: WrappedFieldArrayProps
): JSX.Element => {
  const { fields } = props;
  const { children, initialValue } = props as WrappedFieldArrayProps & {
    children: (fieldName: string) => React.ReactNode;
    initialValue: unknown;
  };

  function addItem(): void {
    /*
     * This is not a mutator, it dispatches an action which updates the state
     * in Redux.
     */
    // eslint-disable-next-line fp/no-mutating-methods
    fields.push(initialValue);
  }

  return (
    <React.Fragment>
      {fields.map(
        (fieldName: string, index: number): JSX.Element => {
          function removeItem(): void {
            fields.remove(index);
          }

          return (
            <div className={"flex items-end"} key={fieldName}>
              <div className={"w-80"}>{children(fieldName)}</div>
              <div className={"w-20"}>
                {index > 0 ? (
                  <Button onClick={removeItem}>
                    <Glyphicon glyph={"trash"} />
                  </Button>
                ) : undefined}
              </div>
              <br />
            </div>
          );
        }
      )}
      <div className={"mt4"}>
        <Button onClick={addItem}>
          <Glyphicon glyph={"plus"} />
        </Button>
      </div>
    </React.Fragment>
  );
};

export { ArrayWrapper };
