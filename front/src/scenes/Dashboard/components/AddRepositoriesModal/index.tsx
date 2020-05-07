/* tslint:disable jsx-no-multiline-js
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Field, FieldArray, InjectedFormProps, WrappedFieldArrayProps } from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { dropdownField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { maxLength, required, validField } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm";
import { default as style } from "./index.css";

export interface IAddRepositoriesModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

const maxRepoUrlLength: ConfigurableValidator = maxLength(150);
const renderReposFields: React.FC<WrappedFieldArrayProps> = (props: WrappedFieldArrayProps): JSX.Element => {
  const addItem: (() => void) = (): void => {
    props.fields.push({ urlRepo: "", branch: "" });
  };

  return (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => {
        const removeItem: (() => void) = (): void => { props.fields.remove(index); };

        return (
          <React.Fragment key={index}>
            {index > 0 ? <React.Fragment><br /><hr /></React.Fragment> : undefined}
            <Row>
              <Col md={3}>
                <label>
                  <label style={{ color: "#f22" }}>* </label>
                  {translate.t("search_findings.tab_resources.protocol")}
                </label>
                <Field name={`${fieldName}.protocol`} component={dropdownField} validate={[required]} >
                  <option value="" selected={true} />
                  <option value="HTTPS">{translate.t("search_findings.tab_resources.https")}</option>
                  <option value="SSH">{translate.t("search_findings.tab_resources.ssh")}</option>
                </Field>
              </Col>
              <Col md={7}>
                <label>
                  <label style={{ color: "#f22" }}>* </label>
                  {translate.t("search_findings.tab_resources.repository")}
                </label>
                <Field
                  name={`${fieldName}.urlRepo`}
                  component={textField}
                  placeholder={translate.t("search_findings.tab_resources.base_url_placeholder")}
                  type="text"
                  validate={[required, validField, maxRepoUrlLength]}
                />
              </Col>
            </Row>
            <Row>
              <Col md={5}>
                <label>
                  <label style={{ color: "#f22" }}>* </label>
                  {translate.t("search_findings.tab_resources.branch")}
                </label>
                <Field
                  name={`${fieldName}.branch`}
                  component={textField}
                  placeholder={translate.t("search_findings.tab_resources.branch_placeholder")}
                  type="text"
                  validate={[required, validField]}
                />
              </Col>
              {index > 0 ? (
                <Col mdOffset={5} md={2} className={style.removeBtn}>
                  <Button bsStyle="primary" onClick={removeItem}>
                    <Glyphicon glyph="trash" />
                  </Button>
                </Col>
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

const addRepositoriesModal: React.FC<IAddRepositoriesModalProps> = (props: IAddRepositoriesModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;

  return (
    <React.StrictMode>
      <Modal
        open={props.isOpen}
        headerTitle={translate.t("search_findings.tab_resources.modal_repo_title")}
        footer={<div />}
      >
        <GenericForm
          name="addRepos"
          initialValues={{ resources: [{ urlRepo: "", branch: "" }] }}
          onSubmit={onSubmit}
        >
          {({ pristine }: InjectedFormProps): JSX.Element => (
            <React.Fragment>
              <FieldArray name="resources" component={renderReposFields} />
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

export { addRepositoriesModal as AddRepositoriesModal };
