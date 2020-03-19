import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { BaseFieldProps, Field } from "redux-form";
import { default as style } from "./index.css";

type EditableFieldProps = BaseFieldProps & {
  alignField?: string;
  className?: string;
  currentValue: string;
  label: string;
  renderAsEditable: boolean;
  type?: string;
  visible?: boolean;
  visibleWhileEditing?: boolean;
};

const renderCurrentValue: ((value: string) => JSX.Element) = (value: string): JSX.Element => {
  const isUrl: boolean = _.startsWith(value, "https://");

  return isUrl
    ? <a href={value} rel="noopener" target="_blank">{value}</a>
    : <p className={style.currentValue}>{value}</p>;
};

const renderHorizontal: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <FormGroup>
        <Col md={3} xs={12} sm={12} className={style.title}><ControlLabel><b>{label}</b></ControlLabel></Col>
        <Col md={9} xs={12} sm={12}>
          {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue)}
        </Col>
      </FormGroup>
    );
  };

const renderHorizontalWide: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <Row className={style.horizontalRow}>
        <Col md={6} xs={12} sm={12} className={style.title}><ControlLabel><b>{label}</b></ControlLabel></Col>
        <Col md={6} xs={12} sm={12}>
          {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue)}
        </Col>
      </Row>
    );
  };

const renderVertical: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <FormGroup>
        <ControlLabel><b>{label}</b></ControlLabel><br />
        {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue)}
      </FormGroup>
    );
  };

const editableField: React.FC<EditableFieldProps> = (props: EditableFieldProps): JSX.Element => {
  let render: JSX.Element;
  if (props.alignField === "horizontal") {
    render = renderHorizontal(props);
  } else if (props.alignField === "horizontalWide") {
    render = renderHorizontalWide(props);
  } else {
    render = renderVertical(props);
  }

  const shouldRender: boolean = _.isUndefined(props.visibleWhileEditing)
    ? props.visible === true
    : props.renderAsEditable
      ? props.visibleWhileEditing
      : !_.isEmpty(props.currentValue);

  return shouldRender ? (render) : <React.Fragment />;
};

editableField.defaultProps = {
  visible: true,
};

export { editableField as EditableField };
