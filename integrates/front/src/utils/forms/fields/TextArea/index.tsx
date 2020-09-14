/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  -------
  We need className to override default styles from react-bootstrap and props
  spreading is the best way to pass down props.
*/
import React from "react";
import _ from "lodash";
import style from "utils/forms/index.css";
import {
  Badge,
  FormControl,
  FormControlProps,
  HelpBlock,
} from "react-bootstrap";
import { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface ITextAreaProps extends WrappedFieldProps, FormControlProps {
  input: { value: string } & Omit<WrappedFieldInputProps, "value">;
  withCount?: boolean;
}

export const TextArea: React.FC<ITextAreaProps> = (
  // Readonly utility type does not work on deeply nested types
  // eslint-disable-next-line @typescript-eslint/prefer-readonly-parameter-types
  props: Readonly<ITextAreaProps>
): JSX.Element => {
  const { input, withCount = false, meta, className } = props;
  const { error, touched } = meta;
  const { value } = input;

  return (
    <React.Fragment>
      <FormControl
        componentClass={"textarea"}
        {...props}
        {...input}
        className={`${style.formControl} ${
          _.isUndefined(className) ? "" : className
        }`}
      />
      {withCount && (
        <Badge className={style.badge} pullRight={true}>
          {value.length}
        </Badge>
      )}
      {withCount && !_.isUndefined(error) && <br />}
      {touched && !_.isUndefined(error) && (
        <HelpBlock className={style.validationError} id={"validationError"}>
          {error as string}
        </HelpBlock>
      )}
    </React.Fragment>
  );
};
