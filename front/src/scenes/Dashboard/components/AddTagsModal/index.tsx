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
import { default as Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import { textField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { required, validTag } from "../../../../utils/validations";

export interface IAddTagsModalProps {
  isOpen: boolean;
  onClose(): void;
  onSubmit(values: {}): void;
}

type formProps = IAddTagsModalProps & InjectedFormProps<{}, IAddTagsModalProps>;

const renderDeleteFieldButton: ((props: FieldArrayFieldsProps<undefined>, index: number) => JSX.Element) =
  (props: FieldArrayFieldsProps<undefined>, index: number): JSX.Element => (
    <Col md={2} style={{ marginTop: "40px" }}>
      <Button bsStyle="primary" onClick={(): void => { props.remove(index); }}>
        <Glyphicon glyph="trash" />
      </Button>
    </Col>
  );

const renderTagsFields: ((props: WrappedFieldArrayProps<undefined>) => JSX.Element) =
  (props: WrappedFieldArrayProps<undefined>): JSX.Element => (
    <React.Fragment>
      {props.fields.map((fieldName: string, index: number) => (
        <Row key={index}>
          <Col md={10}>
            <label>
              <label style={{ color: "#f22" }}>* </label>
              Tag
            </label>
            <Field name={fieldName} component={textField} type="text" validate={[required, validTag]} />
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

const renderTagsForm: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <form onSubmit={props.handleSubmit}>
        <FieldArray name="tags" component={renderTagsFields} />
        {renderFooter(props)}
      </form>
    </React.Fragment>
  );

type tagsForm =
  DecoratedComponentClass<{}, IAddTagsModalProps & Partial<ConfigProps<{}, IAddTagsModalProps>>, string>;

/* tslint:disable:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */

const TagsForm: tagsForm = reduxForm<{}, IAddTagsModalProps>({
  enableReinitialize: true,
  form: "addTags",
  initialValues: {
    tags: [""],
  },
  onSubmitFail: focusError,
})(renderTagsForm);
// tslint:enable:variable-name

export const addTagsModal: React.SFC<IAddTagsModalProps> =
  (props: IAddTagsModalProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={translate.t("search_findings.tab_indicators.tags.modal_title")}
          content={(<TagsForm {...props} />)}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
