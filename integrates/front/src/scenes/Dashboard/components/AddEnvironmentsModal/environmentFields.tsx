import { Button } from "components/Button";
import type { ConfigurableValidator } from "revalidate";
import { Field } from "redux-form";
import { Glyphicon } from "react-bootstrap";
import React from "react";
import type { StyledComponent } from "styled-components";
import { TextArea } from "utils/forms/fields";
import type { WrappedFieldArrayProps } from "redux-form";
import styled from "styled-components";
import { translate } from "utils/translations/translate";
import { RequiredField, Row } from "styles/styledComponents";
import { maxLength, required, validField } from "utils/validations";

const maxCharCount: number = 500;
const maxEnvUrlLength: ConfigurableValidator = maxLength(maxCharCount);

const TextFieldCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "fl ph2 relative w-80",
})``;

const RemoveBtnCol: StyledComponent<
  "div",
  Record<string, unknown>
> = styled.div.attrs<{
  className: string;
}>({
  className: "fl w-20 mt5 relative ph2",
})``;

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
              <TextFieldCol>
                <label>
                  <RequiredField>{"* "}</RequiredField>
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
              </TextFieldCol>
              {index > 0 && (
                // Classname used to override default bootstrap styles.
                // eslint-disable-next-line react/forbid-component-props
                <RemoveBtnCol>
                  <Button onClick={removeItem}>
                    <Glyphicon glyph={"trash"} />
                  </Button>
                </RemoveBtnCol>
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
