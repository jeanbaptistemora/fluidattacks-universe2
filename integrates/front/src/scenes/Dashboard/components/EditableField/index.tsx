import _ from "lodash";
import React, { TextareaHTMLAttributes } from "react";
import { BaseFieldProps, Field } from "redux-form";

import { TooltipWrapper } from "components/TooltipWrapper";
import { default as style } from "scenes/Dashboard/components/EditableField/index.css";
import {
  Col50,
  ControlLabel,
  EditableFieldContent,
  EditableFieldNotUrl,
  EditableFieldTitle25,
  EditableFieldTitle50,
  FormGroup,
  Row,
} from "styles/styledComponents";

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
    : <EditableFieldNotUrl>{value}</EditableFieldNotUrl>;
};

const renderHorizontal: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, tooltip, ...fieldProps } = props;

    return (
      <FormGroup>
        <Row>
          <EditableFieldTitle25>
            <ControlLabel><b>{label}</b></ControlLabel>
          </EditableFieldTitle25>
          <EditableFieldContent>
            {renderAsEditable
              ? <Field {...fieldProps} />
              : _.isUndefined(tooltip) || _.isEmpty(tooltip)
                ? renderCurrentValue(currentValue)
                : <TooltipWrapper message={tooltip} placement="right">
                    {renderCurrentValue(currentValue)}
                  </TooltipWrapper>
            }
          </EditableFieldContent>
        </Row>
      </FormGroup>
    );
  };

const renderHorizontalWide: ((props: EditableFieldProps) => JSX.Element) =
  (props: EditableFieldProps): JSX.Element => {
    const { label, currentValue, renderAsEditable, ...fieldProps } = props;

    return (
      <Row>
        <EditableFieldTitle50><ControlLabel><b>{label}</b></ControlLabel></EditableFieldTitle50>
        <Col50>
          {renderAsEditable ? <Field {...fieldProps} /> : renderCurrentValue(currentValue)}
        </Col50>
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
