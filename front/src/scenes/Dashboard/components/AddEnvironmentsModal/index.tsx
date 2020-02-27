/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Field, FieldArray, InjectedFormProps, WrappedFieldArrayProps } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";

export interface IAddEnvironmentsModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

const renderEnvsFields: React.FC<WrappedFieldArrayProps> = (props: WrappedFieldArrayProps): JSX.Element => {
  const addItem: (() => void) = (): void => {
    props.fields.push({ urlRepo: "", branch: "" });
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
                {translate.t("search_findings.tab_resources.environment")}
              </label>
              <Field name={`${fieldName}.urlEnv`} component={textAreaField} type="text" validate={[required]} />
            </Col>
            {index > 0 ? (
              <Col md={2} style={{ marginTop: "40px" }}>
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

const addEnvironmentsModal: React.FC<IAddEnvironmentsModalProps> = (props: IAddEnvironmentsModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_resources.modal_env_title")}
        footer={<div />}
      >
        <GenericForm
          name="addEnvs"
          initialValues={{ resources: [{ urlEnv: "" }] }}
          onSubmit={onSubmit}
        >
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray name="resources" component={renderEnvsFields} />
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

export { addEnvironmentsModal as AddEnvironmentsModal };
