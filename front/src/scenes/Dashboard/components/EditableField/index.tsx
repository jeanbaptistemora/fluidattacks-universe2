import _ from "lodash";
import React from "react";
import { ControlLabel, FormGroup } from "react-bootstrap";
import { BaseFieldProps, Field, GenericFieldHTMLAttributes } from "redux-form";
import style from "./index.css";

type EditableFieldProps = BaseFieldProps & GenericFieldHTMLAttributes & {
  currentValue: string | number;
  label: string;
  renderAsEditable: boolean;
  visible?: boolean;
};

const renderCurrentValue: ((value: string) => JSX.Element) = (value: string): JSX.Element => {
  const isUrl: boolean = _.startsWith(value, "https://");

  return isUrl ? <a href={value}>{value}</a> : <p className={style.currentValue}>{value}</p>;
};

const editableField: React.SFC<EditableFieldProps> = (props: EditableFieldProps): JSX.Element => {
  const { label, currentValue, renderAsEditable, visible, ...fieldProps } = props;

  return visible === true ? (
    <FormGroup>
      <ControlLabel><b>{label}</b></ControlLabel><br />
      {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue.toString())}
    </FormGroup>
  ) : <React.Fragment />;
};

editableField.defaultProps = {
  visible: true,
};

export { editableField as EditableField };
