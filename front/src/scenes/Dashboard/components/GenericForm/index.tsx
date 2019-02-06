import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Provider } from "react-redux";
import {
  BaseFieldProps, ConfigProps, DecoratedComponentClass,
  Field, GenericFieldHTMLAttributes, InjectedFormProps,
  reduxForm,
} from "redux-form";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";
import style from "./index.css";

export interface IEditableField {
  componentProps?: GenericFieldHTMLAttributes & BaseFieldProps;
  customElement?: JSX.Element;
  label: string;
  renderAsEditable?: boolean;
  value?: string;
  visible: boolean;
}

export type FormCols = IEditableField[];
export type FormRows = FormCols[];

export interface IGenericFormProps {
  form: string;
  formStructure: FormRows;
  initialValues?: {};
  onSubmit(values: {}): void;
}

type formProps = IGenericFormProps & InjectedFormProps<{}, IGenericFormProps>;

const renderCurrentValue: ((fieldProps: IEditableField) => JSX.Element) =
  (fieldProps: IEditableField): JSX.Element => (
    _.startsWith(fieldProps.value, "https://")
      ? <a href={fieldProps.value}>{fieldProps.value}</a>
      : <p style={{ fontSize: "18px" }}>{fieldProps.value}</p>
  );

const renderEditableField: ((fieldProps: IEditableField) => JSX.Element) =
  (fieldProps: IEditableField): JSX.Element =>
    fieldProps.renderAsEditable === true && fieldProps.componentProps !== undefined
      ? <Field {...fieldProps.componentProps} />
      : renderCurrentValue(fieldProps);

const renderField: ((fieldProps: IEditableField, totalCols: number) => JSX.Element) =
  (fieldProps: IEditableField, totalCols: number): JSX.Element => (
    <React.Fragment>
      <Col md={Math.round(12 / totalCols)} xs={12} sm={12} className={style.fieldColumn}>
        <label><b>{fieldProps.label}</b></label><br />
        {fieldProps.componentProps === undefined ? fieldProps.customElement : renderEditableField(fieldProps)}
      </Col>
    </React.Fragment>
  );

const renderCols: ((cols: FormCols) => JSX.Element) = (cols: FormCols): JSX.Element => {
  const visibleCols: FormCols = cols.filter((field: IEditableField) => field.visible);

  return (
    <Row className={style.row}>
      {visibleCols.map((field: IEditableField): JSX.Element => renderField(field, cols.length))}
    </Row>
  );
};

const renderForm: ((props: formProps) => JSX.Element) = (props: formProps): JSX.Element => (
  <React.Fragment>
    <form onSubmit={props.handleSubmit}>
      {props.formStructure.map(renderCols)}
    </form>
  </React.Fragment>
);

type wrappedForm = DecoratedComponentClass<{}, IGenericFormProps & Partial<ConfigProps<{}, IGenericFormProps>>, string>;
/* tslint:disable-next-line:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const WrappedForm: wrappedForm = reduxForm<{}, IGenericFormProps>({})(renderForm);

const genericForm: React.SFC<IGenericFormProps> = (props: IGenericFormProps): JSX.Element => (
  <Provider store={store}>
    <WrappedForm
      enableReinitialize={props.initialValues !== undefined}
      onSubmitFail={focusError}
      {...props}
    />
  </Provider>
);

export { genericForm as GenericForm };
