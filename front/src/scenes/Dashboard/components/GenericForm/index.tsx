/* tslint:disable:jsx-no-lambda
 * Disabling this rule is necessary for binding the form submit function
 */

import React from "react";
import { Form } from "react-bootstrap";
import { Provider } from "react-redux";
import { ConfigProps, DecoratedComponentClass, InjectedFormProps, reduxForm } from "redux-form";
import store from "../../../../store/index";
import { focusError } from "../../../../utils/forms/events";

interface IFormProps {
  children: React.ReactChild;
  initialValues?: {};
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
const WrappedForm: wrappedForm = reduxForm<{}, Pick<IFormProps, "children">>({})
  ((props: formProps) => <Form onSubmit={props.handleSubmit}>{props.children}</Form>);

const genericForm: ((props: IFormProps) => JSX.Element) = (props: IFormProps): JSX.Element => (
  <Provider store={store}>
    <WrappedForm
      enableReinitialize={props.initialValues !== undefined}
      form={props.name}
      initialValues={props.initialValues}
      onSubmit={(values: {}): void => { props.onSubmit(values); }}
      onSubmitFail={focusError}
    >
      {props.children}
    </WrappedForm>
  </Provider>
);

export { genericForm as GenericForm };
