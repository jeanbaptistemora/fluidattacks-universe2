import _ from "lodash";
import React from "react";
import { Col, ControlLabel, FormGroup } from "react-bootstrap";
import { BaseFieldProps, Field, GenericFieldHTMLAttributes } from "redux-form";
import style from "./index.css";

type EditableFieldProps = BaseFieldProps & GenericFieldHTMLAttributes & {
  alignField?: string;
  currentValue: string | number;
  label: string;
  renderAsEditable: boolean;
  visible?: boolean;
};

const renderCurrentValue: ((value: string) => JSX.Element) = (value: string): JSX.Element => {
  const isUrl: boolean = _.startsWith(value, "https://");

  return isUrl ? <a href={value}>{value}</a> : <p className={style.currentValue}>{value}</p>;
};

const renderHorizontal: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <FormGroup>
        <Col md={3} xs={12} sm={12} className={style.title}><ControlLabel><b>{label}</b></ControlLabel></Col>
        <Col md={9} xs={12} sm={12}>
          {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue.toString())}
        </Col>
      </FormGroup>
    );
};

const renderVertical: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <FormGroup>
        <ControlLabel><b>{label}</b></ControlLabel><br />
        {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue.toString())}
      </FormGroup>
    );
};

const editableField: React.SFC<EditableFieldProps> = (props: EditableFieldProps): JSX.Element => {
  const { alignField, visible } = props;

  return visible === true ? (
    alignField === "horizontal"
      ? renderHorizontal(props)
      : renderVertical(props)
  ) : <React.Fragment />;
};

editableField.defaultProps = {
  visible: true,
};

export { editableField as EditableField };
