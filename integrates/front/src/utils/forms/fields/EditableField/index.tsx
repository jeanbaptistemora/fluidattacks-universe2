import type { FieldAttributes } from "formik";
import { Field } from "formik";
import _ from "lodash";
import React from "react";

import { ExternalLink } from "components/ExternalLink";
import { Tooltip } from "components/Tooltip";
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

/* eslint-disable @typescript-eslint/no-explicit-any, react/require-default-props, react/no-unused-prop-types */
interface IEditableFieldProps extends FieldAttributes<any> {
  alignField?: string;
  className?: string;
  currentValue: string;
  id?: string;
  label: string;
  renderAsEditable: boolean;
  tooltip?: string;
  type?: string;
  visibleWhileEditing?: boolean;
}
/* eslint-enable @typescript-eslint/no-explicit-any, react/require-default-props, react/no-unused-prop-types */

const renderCurrentValue: (value: string) => JSX.Element = (
  value: string
): JSX.Element => {
  const isUrl: boolean = _.startsWith(value, "https://");

  return isUrl ? (
    <ExternalLink href={value}>{value}</ExternalLink>
  ) : (
    <EditableFieldNotUrl>{value}</EditableFieldNotUrl>
  );
};

const renderHorizontal: (props: IEditableFieldProps) => JSX.Element = (
  props: IEditableFieldProps
): JSX.Element => {
  const {
    id = "editableField",
    label,
    currentValue,
    renderAsEditable,
    tooltip,
    ...fieldProps // eslint-disable-line fp/no-rest-parameters
  } = props;

  if (renderAsEditable) {
    return (
      <FormGroup>
        <Row>
          <EditableFieldTitle25>
            <ControlLabel>
              <b>{label}</b>
            </ControlLabel>
          </EditableFieldTitle25>
          <EditableFieldContent>
            {/* eslint-disable-next-line react/jsx-props-no-spreading */}
            <Field {...fieldProps} />
          </EditableFieldContent>
        </Row>
      </FormGroup>
    );
  }

  return (
    <FormGroup>
      <Row>
        <EditableFieldTitle25>
          <ControlLabel>
            <b>{label}</b>
          </ControlLabel>
        </EditableFieldTitle25>
        <EditableFieldContent>
          {_.isUndefined(tooltip) || _.isEmpty(tooltip) ? (
            renderCurrentValue(currentValue)
          ) : (
            <Tooltip disp={"block"} id={id} place={"right"} tip={tooltip}>
              {renderCurrentValue(currentValue)}
            </Tooltip>
          )}
        </EditableFieldContent>
      </Row>
    </FormGroup>
  );
};

const renderHorizontalWide: (props: IEditableFieldProps) => JSX.Element = (
  props: IEditableFieldProps
): JSX.Element => {
  // eslint-disable-next-line fp/no-rest-parameters
  const { label, currentValue, renderAsEditable, ...fieldProps } = props;

  return (
    <Row>
      <EditableFieldTitle50>
        <ControlLabel>
          <b>{label}</b>
        </ControlLabel>
      </EditableFieldTitle50>
      <Col50>
        {renderAsEditable ? (
          <Field {...fieldProps} /> // eslint-disable-line react/jsx-props-no-spreading
        ) : (
          renderCurrentValue(currentValue)
        )}
      </Col50>
    </Row>
  );
};

const renderVertical: (props: IEditableFieldProps) => JSX.Element = (
  props: IEditableFieldProps
): JSX.Element => {
  const {
    id = "editableField",
    label,
    currentValue,
    renderAsEditable,
    tooltip,
    ...fieldProps // eslint-disable-line fp/no-rest-parameters
  } = props;

  if (_.isUndefined(tooltip)) {
    return (
      <FormGroup>
        <React.Fragment>
          <ControlLabel>
            <b>{label}</b>
          </ControlLabel>
          <br />
          {renderAsEditable ? (
            <Field {...fieldProps} /> // eslint-disable-line react/jsx-props-no-spreading
          ) : (
            renderCurrentValue(currentValue)
          )}
        </React.Fragment>
      </FormGroup>
    );
  }

  return (
    <FormGroup>
      {renderAsEditable ? (
        <React.Fragment>
          <ControlLabel>
            <b>{label}</b>
          </ControlLabel>
          <br />
          <Tooltip id={id} tip={tooltip}>
            {/* eslint-disable-next-line react/jsx-props-no-spreading */}
            <Field {...fieldProps} />{" "}
          </Tooltip>
        </React.Fragment>
      ) : (
        <React.Fragment>
          <Tooltip disp={"inline-block"} id={id} place={"top"} tip={tooltip}>
            <ControlLabel>
              <b>{label}</b>
            </ControlLabel>
          </Tooltip>
          <br />
          {renderCurrentValue(currentValue)}
        </React.Fragment>
      )}
    </FormGroup>
  );
};

const EditableField: React.FC<IEditableFieldProps> = (
  props: IEditableFieldProps
): JSX.Element => {
  const { alignField, currentValue, renderAsEditable, visibleWhileEditing } =
    props;

  function setRender(
    properties: IEditableFieldProps,
    alignF: string
  ): JSX.Element {
    if (alignF === "horizontal") {
      return renderHorizontal(properties);
    } else if (alignF === "horizontalWide") {
      return renderHorizontalWide(properties);
    }

    return renderVertical(properties);
  }

  const render: JSX.Element = setRender(props, alignField as string);

  const isVisibleWhileEditing: boolean =
    visibleWhileEditing === true || _.isUndefined(visibleWhileEditing);

  const shouldRender: boolean = renderAsEditable
    ? isVisibleWhileEditing
    : !_.isEmpty(currentValue) && currentValue !== "0";

  return shouldRender ? render : <div />;
};

export { EditableField };
