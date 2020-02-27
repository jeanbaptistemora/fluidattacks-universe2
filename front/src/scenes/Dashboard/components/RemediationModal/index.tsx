/* tslint:disable jsx-no-multiline-js jsx-no-lambda
 * JSX-NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
 * readability of the code that dynamically renders the fields
 * JSX-NO-LAMBDA: Disabling this rule is necessary for the sake of simplicity and
 * readability of the code that binds click events
 */

import React from "react";
import { ButtonToolbar, ControlLabel, FormGroup } from "react-bootstrap";
import { Provider } from "react-redux";
import {
  ConfigProps, DecoratedComponentClass, Field, InjectedFormProps, reduxForm,
} from "redux-form";
import { ConfigurableValidator } from "revalidate";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import store from "../../../../store/index";
import { default as globalStyle } from "../../../../styles/global.css";
import { textAreaField } from "../../../../utils/forms/fields";
import translate from "../../../../utils/translations/translate";
import { minLength, required } from "../../../../utils/validations";

export interface IAddRemediationProps {
  additionalInfo?: string;
  isLoading: boolean;
  isOpen: boolean;
  message: string;
  title: string;
  children?(): JSX.Element;
  onClose(): void;
  onSubmit(values: {}): void;
}

type formProps = IAddRemediationProps & InjectedFormProps<{}, IAddRemediationProps>;

const renderFooter: ((props: formProps) => JSX.Element) =
  (props: formProps): JSX.Element => (
    <React.Fragment>
      <ButtonToolbar className="pull-right">
        <Button bsStyle="default" onClick={(): void => { props.onClose(); }}>
          {translate.t("confirmmodal.cancel")}
        </Button>
        <Button bsStyle="primary" type="submit" disabled={props.pristine || props.submitting || props.isLoading}>
          {translate.t("confirmmodal.proceed")}
        </Button>
      </ButtonToolbar>
    </React.Fragment>
  );

const minJustificationLength: ConfigurableValidator = minLength(50);
const renderFields: ((props: formProps) => JSX.Element) = (props: formProps): JSX.Element => (
  <React.Fragment>
    <form onSubmit={props.handleSubmit}>
      {props.children === undefined ? undefined : props.children()}
      <FormGroup>
        <ControlLabel>
          <label style={{ color: "#f22" }}>* </label>
          {props.message}
        </ControlLabel>
        <Field
          name="treatmentJustification"
          type="text"
          className={globalStyle.noResize}
          component={textAreaField}
          min={100}
          validate={[required, minJustificationLength]}
          withCount={true}
          rows="6"
        />
      </FormGroup>
      {props.additionalInfo}
      <br />
      {renderFooter(props)}
    </form>
  </React.Fragment>
);

type remediationForm =
  DecoratedComponentClass<{}, IAddRemediationProps & Partial<ConfigProps<{}, IAddRemediationProps>>, string>;

/* tslint:disable-next-line:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const Form: remediationForm = reduxForm<{}, IAddRemediationProps>({ form: "addRemediation" })(renderFields);

export const remediationModal: React.FC<IAddRemediationProps> =
  (props: IAddRemediationProps): JSX.Element => (
    <React.StrictMode>
      <Provider store={store}>
        <Modal
          open={props.isOpen}
          headerTitle={props.title}
          content={<Form {...props} />}
          footer={<div />}
        />
      </Provider>
    </React.StrictMode>
  );
