/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { ButtonToolbar, Col, Glyphicon, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import {
  ConfigProps, DecoratedComponentClass, Field,
  FieldArray, FieldArrayFieldsProps, InjectedFormProps,
  reduxForm,
  WrappedFieldArrayProps,
} from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import { dropdownField, textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";
import { default as style } from "./index.css";

export interface IAddRepositoriesModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

type formProps = IAddRepositoriesModalProps & InjectedFormProps<{}, IAddRepositoriesModalProps>;

const renderDeleteFieldButton: ((props: FieldArrayFieldsProps<undefined>, index: number) => JSX.Element) =
  (props: FieldArrayFieldsProps<undefined>, index: number): JSX.Element => (
    <Col mdOffset={5} md={2} style={{ marginTop: "40px" }}>
      <Button bsStyle="primary" onClick={(): void => { props.remove(index); }}>
        <Glyphicon glyph="trash" />
      </Button>
    </Col>
  );

const renderReposFields: ((props: WrappedFieldArrayProps<undefined>) => JSX.Element) =
  (props: WrappedFieldArrayProps<undefined>): JSX.Element => (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => (
        <Row key={index}>
          <Col md={12}>
            { index > 0 ?
              <React.Fragment>
                <br />
                <hr />
              </React.Fragment>
              : undefined
            }
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
                  validate={[required]}
                />
              </Col>
            </Row>
            <Row className={style.padding_top}>
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
                  validate={[required]}
                />
              </Col>
              {index > 0 ? renderDeleteFieldButton(props.fields, index) : undefined}
            </Row>
          </Col>
        </Row>
      ))}
      <br />
      <Button
        bsStyle="primary"
        onClick={(): void => { props.fields.push(undefined); }}
      >
        <Glyphicon glyph="plus" />
      </Button>
    </React.Fragment>
  );

const renderFooter: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <ButtonToolbar className="pull-right">
        <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
          {translate.t("confirmmodal.cancel")}
        </Button>
        <Button bsStyle="primary" type="submit" disabled={props.pristine || props.submitting}>
          {translate.t("confirmmodal.proceed")}
        </Button>
      </ButtonToolbar>
    </React.Fragment>
  );

const renderReposForm: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <form onSubmit={props.handleSubmit}>
        <FieldArray name="resources" component={renderReposFields} />
        {renderFooter(props)}
      </form>
    </React.Fragment>
  );

type resourcesForm = DecoratedComponentClass<
  {}, IAddRepositoriesModalProps & Partial<ConfigProps<{}, IAddRepositoriesModalProps>>, string>;

/* tslint:disable:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const ReposForm: resourcesForm = reduxForm<{}, IAddRepositoriesModalProps>({
  enableReinitialize: true,
  form: "addRepos",
  initialValues: {
    resources: [{ urlRepo: "", branch: "" }],
  },
  onSubmitFail: focusError,
})(renderReposForm);
// tslint:enable:variable-name

export const addRepositoriesModal: React.FC<IAddRepositoriesModalProps> =
  (props: IAddRepositoriesModalProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={translate.t("search_findings.tab_resources.modal_repo_title")}
          content={(<ReposForm {...props} />)}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
