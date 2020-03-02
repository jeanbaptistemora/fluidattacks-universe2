/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Field, FieldArray, InjectedFormProps, WrappedFieldArrayProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required, validTag } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
import { default as style } from "./index.css";

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
        <Row key={index}>
          <Col md={10}>
            <label>
              <label style={{ color: "#f22" }}>* </label>
              Tag
            </label>
            <Field name={fieldName} component={textField} type="text" validate={[required, validTag]} />
          </Col>
          {index > 0 ? (
            <Col md={2} className={style.removeBtn}>
              <Button bsStyle="primary" onClick={removeItem}>
                <Glyphicon glyph="trash" />
              </Button>
            </Col>
          ) : undefined}
        </Row>
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
        footer={<div />}
      >
        <GenericForm name="addTags" initialValues={{ tags: [""] }} onSubmit={onSubmit}>
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray name="tags" component={renderTagsFields} />
              <ButtonToolbar className="pull-right">
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
