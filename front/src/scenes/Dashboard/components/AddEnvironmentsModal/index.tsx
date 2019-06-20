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
  FieldArray, FieldArrayFieldsProps, GenericFieldArray, InjectedFormProps,
  reduxForm,
  WrappedFieldArrayProps,
} from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import { textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required } from "../../../../utils/validations";

export interface IAddEnvironmentsModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

/* This is necessary because there is a problem with the type of FieldArray in redux-form library,
* this is the issue: https://github.com/DefinitelyTyped/DefinitelyTyped/issues/32858#issuecomment-461441222
*/
/* tslint:disable-next-line:variable-name
* Disabling here is necessary due a conflict
* between lowerCamelCase var naming rule from tslint
* and PascalCase rule for naming JSX elements
*/
const FieldArrayCustom: new () => GenericFieldArray<Field<React.InputHTMLAttributes<HTMLInputElement> |
  React.SelectHTMLAttributes<HTMLSelectElement> | React.TextareaHTMLAttributes<HTMLTextAreaElement>>,
  WrappedFieldArrayProps<undefined>> = FieldArray as new () =>
  GenericFieldArray<Field, WrappedFieldArrayProps<undefined>>;

type formProps = IAddEnvironmentsModalProps & InjectedFormProps<{}, IAddEnvironmentsModalProps>;

const renderDeleteFieldButton: ((props: FieldArrayFieldsProps<undefined>, index: number) => JSX.Element) =
  (props: FieldArrayFieldsProps<undefined>, index: number): JSX.Element => (
    <Col md={2} style={{ marginTop: "40px" }}>
      <Button bsStyle="primary" onClick={(): void => { props.remove(index); }}>
        <Glyphicon glyph="trash" />
      </Button>
    </Col>
  );

const renderEnvsFields: ((props: WrappedFieldArrayProps<undefined>) => JSX.Element) =
  (props: WrappedFieldArrayProps<undefined>): JSX.Element => (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => (
        <Row key={index}>
          <Col md={10}>
            <label>
              <label style={{ color: "#f22" }}>* </label>
              {translate.t("search_findings.tab_resources.environment")}
            </label>
            <Field name={`${fieldName}.urlEnv`} component={textAreaField} type="text" validate={[required]} />
          </Col>
          {index > 0 ? renderDeleteFieldButton(props.fields, index) : undefined}
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

const renderEnvsForm: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <form onSubmit={props.handleSubmit}>
        <FieldArrayCustom name="resources" component={renderEnvsFields} />
        {renderFooter(props)}
      </form>
    </React.Fragment>
  );

type resourcesForm = DecoratedComponentClass<
    {}, IAddEnvironmentsModalProps & Partial<ConfigProps<{}, IAddEnvironmentsModalProps>>, string>;

/* tslint:disable:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */

const EnvsForm: resourcesForm = reduxForm<{}, IAddEnvironmentsModalProps>({
  enableReinitialize: true,
  form: "addEnvs",
  initialValues: {
    resources: [{ urlEnv: "" }],
  },
  onSubmitFail: focusError,
})(renderEnvsForm);

// tslint:enable:variable-name

export const addEnvironmentsModal: React.FC<IAddEnvironmentsModalProps> =
  (props: IAddEnvironmentsModalProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={translate.t("search_findings.tab_resources.modal_env_title")}
          content={<EnvsForm {...props} />}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
