/* eslint-disable react/forbid-component-props, react/jsx-props-no-spreading
  -------
  We need className to override default styles from react-bootstrap and props
  spreading is the best way to pass down props.
*/
import React from "react";
import { ValidationError } from "styles/styledComponents";
import _ from "lodash";
import style from "utils/forms/index.css";
import type { WrappedFieldInputProps, WrappedFieldProps } from "redux-form";

interface ITextAreaProps extends WrappedFieldProps {
  className?: string;
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
      <textarea
        {...props}
        {...input}
        className={`${style["form-control"]} ${style["text-area"]} ${
          _.isUndefined(className) ? "" : className
        }`}
      />
      {withCount ? (
        <div className={style.badge}>{value.length}</div>
      ) : undefined}
      {withCount && !_.isUndefined(error) ? <br /> : undefined}
      {touched && !_.isUndefined(error) ? (
        <ValidationError id={"validationError"}>
          {error as string}
        </ValidationError>
      ) : undefined}
    </React.Fragment>
  );
};
