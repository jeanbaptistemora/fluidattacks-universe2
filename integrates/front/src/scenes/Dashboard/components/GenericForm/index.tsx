/* eslint-disable @typescript-eslint/no-explicit-any */
import React from "react";
import { focusError } from "utils/forms/events";
import { reduxForm } from "redux-form";
import type {
  ConfigProps,
  DecoratedComponentClass,
  InjectedFormProps,
} from "redux-form";

// eslint-disable-next-line @typescript-eslint/no-type-alias
type FormChildren = React.ReactNode | ((props: formProps) => React.ReactNode);

interface IFormProps
  extends Pick<
    ConfigProps<any, Pick<IFormProps, "children">>,
    "initialValues" | "onChange" | "validate"
  > {
  children: FormChildren;
  name: string;
  onSubmit: (values: any) => void;
}

type formProps = Pick<IFormProps, "children"> &
  InjectedFormProps<any, Pick<IFormProps, "children">>;

type wrappedForm = DecoratedComponentClass<
  any,
  Pick<IFormProps, "children"> & ConfigProps<any, Pick<IFormProps, "children">>,
  string
>;

const WrappedForm: wrappedForm = reduxForm<any, Pick<IFormProps, "children">>(
  {}
)(
  (props: formProps): JSX.Element => (
    <form onSubmit={props.handleSubmit}>
      {typeof props.children === "function"
        ? props.children(props)
        : props.children}
    </form>
  )
);

const genericForm: (props: IFormProps) => JSX.Element = (
  props: IFormProps
): JSX.Element => {
  const { initialValues, name, onChange, validate, children, onSubmit } = props;

  return (
    <WrappedForm
      enableReinitialize={initialValues !== undefined}
      form={name}
      initialValues={initialValues}
      onChange={onChange}
      onSubmit={onSubmit}
      onSubmitFail={focusError}
      validate={validate}
    >
      {children}
    </WrappedForm>
  );
};

export { genericForm as GenericForm };
