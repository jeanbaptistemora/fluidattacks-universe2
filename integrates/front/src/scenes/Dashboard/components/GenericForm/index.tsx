import React from "react";
import { ConfigProps, DecoratedComponentClass, InjectedFormProps, reduxForm } from "redux-form";
import { focusError } from "utils/forms/events";

type FormChildren = React.ReactNode | ((props: formProps) => React.ReactNode);

interface IFormProps extends Pick<
  ConfigProps<{}, Pick<IFormProps, "children">>,
  "initialValues" | "onChange" | "validate"
> {
  children: FormChildren;
  name: string;
  onSubmit(values: {}): void;
}

type formProps = Pick<IFormProps, "children"> & InjectedFormProps<{}, Pick<IFormProps, "children">>;

type wrappedForm = DecoratedComponentClass<{}, Pick<IFormProps, "children">
  & ConfigProps<{}, Pick<IFormProps, "children">>, string>;

/* tslint:disable-next-line:variable-name
 * VARIABLE-NAME: Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const WrappedForm: wrappedForm = reduxForm<{}, Pick<IFormProps, "children">>({})((props: formProps) => (
  <form onSubmit={props.handleSubmit}>
    {typeof props.children === "function" ? props.children(props) : props.children}
  </form>
));

const genericForm: ((props: IFormProps) => JSX.Element) = (props: IFormProps): JSX.Element => {
  const handleSubmit: ((values: {}) => void) = (values: {}): void => { props.onSubmit(values); };

  return (
    <WrappedForm
      enableReinitialize={props.initialValues !== undefined}
      form={props.name}
      initialValues={props.initialValues}
      onSubmit={handleSubmit}
      onSubmitFail={focusError}
      onChange={props.onChange}
      validate={props.validate}
    >
      {props.children}
    </WrappedForm>
  );
};

export { genericForm as GenericForm };
