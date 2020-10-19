/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { Glyphicon } from "react-bootstrap";
import { Field, FieldArray, InjectedFormProps, WrappedFieldArrayProps } from "redux-form";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col80,
  ControlLabel,
  RemoveTag,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Text } from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import { required, validTag } from "utils/validations";

export interface IAddTagsModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

const renderTagsFields: React.FC<WrappedFieldArrayProps> = (props: WrappedFieldArrayProps): JSX.Element => {
  const addItem: (() => void) = (): void => {
    props.fields.push("");
  };

  return (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => {
        const removeItem: (() => void) = (): void => { props.fields.remove(index); };

        return (
        <React.Fragment key={index}>
          {index > 0 ? <React.Fragment><br /><hr /></React.Fragment> : undefined}
          <Row>
            <Col80>
              <ControlLabel>
                <RequiredField>{"* "}</RequiredField>
                Tag
              </ControlLabel>
              <Field name={fieldName} component={Text} type="text" validate={[required, validTag]} />
            </Col80>
            {index > 0 ? (
              <RemoveTag>
                <Button onClick={removeItem}>
                  <Glyphicon glyph="trash" />
                </Button>
              </RemoveTag>
            ) : undefined}
          </Row>
        </React.Fragment>
      );
    })}
      <br />
      <Button onClick={addItem}>
        <Glyphicon glyph="plus" />
      </Button>
    </React.Fragment>
  );
};

const addTagsModal: React.FC<IAddTagsModalProps> = (props: IAddTagsModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_indicators.tags.modal_title")}
      >
        <GenericForm name="addTags" initialValues={{ tags: [""] }} onSubmit={onSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray name="tags" component={renderTagsFields} />
              <ButtonToolbar>
                <Button onClick={onClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type="submit" disabled={pristine}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </React.Fragment>
          )}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};

export { addTagsModal as AddTagsModal };
