import { Button } from "components/Button";
import { ConfigurableValidator } from "revalidate";
import React from "react";
import { TextArea } from "utils/forms/fields";
import style from "scenes/Dashboard/components/AddEnvironmentsModal/index.css";
import { translate } from "utils/translations/translate";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { Field, WrappedFieldArrayProps } from "redux-form";
import { maxLength, required, validField } from "utils/validations";

const maxCharCount: number = 400;
const maxEnvUrlLength: ConfigurableValidator = maxLength(maxCharCount);

export const EnvironmentFields: React.FC<WrappedFieldArrayProps> = (
  props: WrappedFieldArrayProps
): JSX.Element => {
  const { fields } = props;

  function addItem(): void {
    /*
     * This is not a mutator, it dispatches an action which updates the state
     * in Redux.
     */
    // eslint-disable-next-line fp/no-mutating-methods
    fields.push({ urlEnv: "" });
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
              <Col md={10}>
                <label>
                  <span className={style.red}>{"* "}</span>
                  {translate.t(
                    "search_findings.tab_resources.environment.text"
                  )}
                </label>
                <Field
                  component={TextArea}
                  name={`${fieldName}.urlEnv`}
                  type={"text"}
                  validate={[required, validField, maxEnvUrlLength]}
                />
              </Col>
              {index > 0 && (
                // Classname used to override default bootstrap styles.
                // eslint-disable-next-line react/forbid-component-props
                <Col className={style.mt} md={2}>
                  <Button onClick={removeItem}>
                    <Glyphicon glyph={"trash"} />
                  </Button>
                </Col>
              )}
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
