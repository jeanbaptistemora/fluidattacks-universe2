import { Button } from "components/Button";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import { Row } from "styles/styledComponents";
import type { WrappedFieldArrayProps } from "redux-form";

const ArrayWrapper: React.FC<WrappedFieldArrayProps> = (
  props: WrappedFieldArrayProps
): JSX.Element => {
  const { fields } = props;
  const { children } = props as WrappedFieldArrayProps & {
    children: (fieldName: string) => React.ReactNode;
  };

  function addItem(): void {
    /*
     * This is not a mutator, it dispatches an action which updates the state
     * in Redux.
     */
    // eslint-disable-next-line fp/no-mutating-methods
    fields.push({});
  }

  return (
    <React.Fragment>
      {fields.map(
        (fieldName: string, index: number): JSX.Element => {
          function removeItem(): void {
            fields.remove(index);
          }

          return (
            <Row key={fieldName}>
              {children(fieldName)}
              {index > 0 ? (
                <Button onClick={removeItem}>
                  <Glyphicon glyph={"trash"} />
                </Button>
              ) : undefined}
            </Row>
          );
        }
      )}
      <br />
      <Button onClick={addItem}>
        <Glyphicon glyph={"plus"} />
      </Button>
    </React.Fragment>
  );
};

export { ArrayWrapper };
