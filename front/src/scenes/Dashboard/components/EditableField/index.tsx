import _ from "lodash";
import React, { TextareaHTMLAttributes } from "react";
import { Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { BaseFieldProps, Field } from "redux-form";
import { TooltipWrapper } from "../../../../components/TooltipWrapper/index";
import { default as style } from "./index.css";

type EditableFieldProps = BaseFieldProps & TextareaHTMLAttributes<HTMLTextAreaElement> & {
  alignField?: string;
  className?: string;
  currentValue: string;
  label: string;
  renderAsEditable: boolean;
  tooltip?: string;
  type?: string;
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
    const { label, currentValue, renderAsEditable, tooltip, ...fieldProps } = props;

    return (
      <FormGroup>
        <Col md={3} xs={12} sm={12} className={style.title}>
          {_.isUndefined(tooltip) || _.isEmpty(tooltip) ? <ControlLabel><b>{label}</b></ControlLabel>
          : (
            <TooltipWrapper message={tooltip} placement="top">
              <ControlLabel><b>{label}</b></ControlLabel>
            </TooltipWrapper>
          )}
        </Col>
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
    const { label, currentValue, renderAsEditable, tooltip, ...fieldProps } = props;

    return (
      <FormGroup>
        { _.isUndefined(tooltip) ? (
          <React.Fragment>
            <ControlLabel><b>{label}</b></ControlLabel><br />
            {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue)}
          </React.Fragment>
        ) : (
          renderAsEditable ? (
            <React.Fragment>
              <ControlLabel><b>{label}</b></ControlLabel><br />
              <TooltipWrapper message={tooltip}>
                <Field {...fieldProps} />
              </TooltipWrapper>
            </React.Fragment>
          ) : (
            <React.Fragment>
              <TooltipWrapper message={tooltip} placement="top">
                <ControlLabel><b>{label}</b></ControlLabel>
              </TooltipWrapper>
              <br />
              {renderCurrentValue(currentValue)}
            </React.Fragment>
          )
        )}
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

  const visibleWhileEditing: boolean = props.visibleWhileEditing === true
   || _.isUndefined(props.visibleWhileEditing);

  const shouldRender: boolean = props.renderAsEditable
    ? visibleWhileEditing
    : !_.isEmpty(props.currentValue) && props.currentValue !== "0";

  return shouldRender ? (render) : <React.Fragment />;
};

export { editableField as EditableField };
