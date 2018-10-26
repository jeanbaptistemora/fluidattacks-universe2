import { AxiosError, AxiosResponse } from "axios";
import _ from "lodash";
import React from "react";
import {
  Button, ButtonToolbar, ControlLabel,
  FormControl, FormControlProps, FormGroup,
  Row,
} from "react-bootstrap";
import {
  ConfigProps, DecoratedComponentClass, Field,
  FormProps, formValueSelector, InjectedFormProps,
  reduxForm, WrappedFieldProps,
} from "redux-form";
import { default as Modal } from "../../../../../components/Modal/index";
import store from "../../../../../store/index";
import { msgError } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import { required, validEmail } from "../../../../../utils/validations";
import Xhr from "../../../../../utils/xhr";
import * as actions from "../../../actions";
import style from "./index.css";

export interface IAddUserModalProps {
  open: boolean;
  projectName: string;
  translations: { [key: string]: string };
  type: "add" | "edit";
  userRole: string;
}

type CustomFormProps = IAddUserModalProps & InjectedFormProps<{}, IAddUserModalProps>;

type CustomFieldProps = FormProps<{}, {}, {}> & FormControlProps & WrappedFieldProps;

/* tslint:disable-next-line:variable-name
 * Disabling here is necessary due a conflict
 * between lowerCamelCase var naming rule from tslint
 * and PascalCase rule for naming JSX elements
 */
const Error: ((arg1: { msg: string }) => JSX.Element) =
  (props: { msg: string }): JSX.Element => (
    <span className={style.validationError}>{props.msg}</span>
);

const formTextField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        id={fieldProps.id}
        type={fieldProps.type}
        placeholder={fieldProps.placeholder}
        min={fieldProps.min}
        max={fieldProps.max}
        value={fieldProps.input.value}
        onChange={fieldProps.input.onChange}
        onBlur={fieldProps.input.onBlur}
        disabled={fieldProps.disabled}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? <Error msg={fieldProps.meta.error as string}/> : undefined}
  </div>
);

const handleDropdownChange: ((arg1: React.FormEvent<FormGroup>, arg2: CustomFieldProps) => void) =
  (event: React.FormEvent<FormGroup>, fieldProps: CustomFieldProps): void => {
  fieldProps.input.onChange((event.target as HTMLInputElement).value);
};

const formDropdownField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <div>
      <FormControl
        componentClass="select"
        children={fieldProps.children}
        /* tslint:disable-next-line jsx-no-lambda
         * Disabling this rule is necessary for the sake of simplicity and
         * readability of the code that binds component events
         */
        onChange={(event: React.FormEvent<FormGroup>): void => { handleDropdownChange(event, fieldProps); }}
      />
      {fieldProps.meta.touched && fieldProps.meta.error ? <Error msg={fieldProps.meta.error as string}/> : undefined}
  </div>
);

const closeModal: ((arg1: CustomFormProps) => void) =
  (props: CustomFormProps): void => {
  store.dispatch(actions.closeUsersMdl());
  /* tslint:disable-next-line no-any
   * Disabling here is necessary because this is a call to a JS function
   * attached to the window object, which is not recognized by TS
   */
  (window as any).intlTelInputGlobals.instances = {};
  props.reset();
};

const loadAutofillData: ((arg1: CustomFormProps) => void) =
  (props: CustomFormProps): void => {
  /* tslint:disable-next-line no-any
   * Disabling here is necessary since forms are
   * a generic component and their fields may differ
   */
  const fieldSelector: ((stateTree: {}, ...fields: string[]) => any) = formValueSelector("addUser");
  const email: string = fieldSelector(store.getState(), "email");
  if (!_.isEmpty(email)) {
    let gQry: string;
    gQry = `{
      userData(projectName: "${props.projectName}", userEmail: "${email}") {
        organization
        responsability
        phoneNumber
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting user information for autofill")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      props.change("organization", data.userData.organization);
      props.change("phone", data.userData.phoneNumber);
      props.change("responsability", data.userData.responsability);
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(props.translations["proj_alerts.error_textsad"]);
        rollbar.error(error.message, errors);
      }
    });
  }
};

const renderManagerRoles: ((arg1: CustomFormProps["translations"]) => JSX.Element) =
  (translations: CustomFormProps["translations"]): JSX.Element => (
  <React.Fragment>
    <option value="customer">{translations["search_findings.tab_users.customer"]}</option>
    <option value="customeradmin">{translations["search_findings.tab_users.customer_admin"]}</option>
  </React.Fragment>
);

const renderAllRoles: ((arg1: CustomFormProps["translations"]) => JSX.Element) =
  (translations: CustomFormProps["translations"]): JSX.Element => (
  <React.Fragment>
    <option value="analyst">{translations["search_findings.tab_users.analyst"]}</option>
    <option value="admin">{translations["search_findings.tab_users.admin"]}</option>
    {renderManagerRoles(translations)}
  </React.Fragment>
);

const requiredIndicator: JSX.Element = <label style={{ color: "#f22"}}>* </label>;

const renderFormContent: ((arg1: CustomFormProps) => JSX.Element) =
  (props: CustomFormProps): JSX.Element => (
  <form onSubmit={props.handleSubmit}>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {props.translations["search_findings.tab_users.textbox"]}
      </ControlLabel>
      <Field
        name="email"
        component={formTextField}
        type="text"
        placeholder={props.translations["search_findings.tab_users.email"]}
        validate={[required, validEmail]}
        disabled={props.type === "edit"}
        /* tslint:disable-next-line jsx-no-lambda
         * Disabling this rule is necessary for the sake of simplicity and
         * readability of the code that binds component events
         */
        onBlur={(): void => { loadAutofillData(props); }}
      />
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {props.translations["search_findings.tab_users.user_organization"]}
      </ControlLabel>
      <Field
        name="organization"
        component={formTextField}
        type="text"
        validate={[required]}
      />
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {props.translations["search_findings.tab_users.role"]}
      </ControlLabel>
      <Field
        name="role"
        component={formDropdownField}
        validate={[required]}
      >
        <option value="" selected={true}/>
        {props.userRole === "admin" ? renderAllRoles(props.translations) : undefined}
        {props.userRole === "customeradmin" ? renderManagerRoles(props.translations) : undefined}
      </Field>
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {props.translations["search_findings.tab_users.user_responsibility"]}
      </ControlLabel>
      <Field
        name="responsability"
        component={formTextField}
        type="text"
        placeholder={props.translations["search_findings.tab_users.responsibility_placeholder"]}
        validate={[required]}
      />
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {props.translations["search_findings.tab_users.phone_number"]}
      </ControlLabel>
      <Field
        name="phone"
        id="phone"
        component={formTextField}
        type="text"
        validate={[required]}
      />
    </FormGroup>
    <Row>
      <ButtonToolbar className="pull-right">
        <Button
          bsStyle="default"
          /* tslint:disable-next-line jsx-no-lambda
           * Disabling this rule is necessary for the sake of simplicity and
           * readability of the code that binds component events
           */
          onClick={(): void => { closeModal(props); }}
        >
          {props.translations["confirmmodal.cancel"]}
        </Button>
        <Button
          bsStyle="primary"
          type="submit"
          disabled={props.pristine || props.submitting}
        >
          {props.translations["confirmmodal.proceed"]}
        </Button>
      </ButtonToolbar>
    </Row>
  </form>
);

export const addUserModal:
DecoratedComponentClass<{}, IAddUserModalProps & Partial<ConfigProps<{}, IAddUserModalProps>>, string> =
  reduxForm<{}, IAddUserModalProps>({
    enableReinitialize: true,
    form: "addUser",
  })((props: CustomFormProps): JSX.Element => {
    /* tslint:disable-next-line no-any
     * Disabling here is necessary because this is a call to a JS function
     * attached to the window object, which is not recognized by TS
     */
    const tsWindow: any = (window as any);
    /* Hack: Initialize and apply intlTelInput plugin from JS since
     * there are currently no 3rd party components compatible
     * with React TS for creating phone number fields
     */
    if (props.open) {
      setTimeout((): void => {
        if (_.isEmpty(tsWindow.intlTelInputGlobals.instances)) {
          tsWindow.intlTelInput(document.querySelector("#phone"), {
            initialCountry: "co",
            separateDialCode: true,
          });
        }
      },         200);
    }
    const title: string = props.type === "add"
    ? props.translations["search_findings.tab_users.title"]
    : props.translations["search_findings.tab_users.edit_user_title"];

    return (
      <React.StrictMode>
        <Modal
          open={props.open}
          headerTitle={title}
          content={renderFormContent(props)}
          footer={<div/>}
        />
      </React.StrictMode>
); });
