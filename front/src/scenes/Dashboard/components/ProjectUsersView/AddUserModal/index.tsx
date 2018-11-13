import { AxiosError, AxiosResponse } from "axios";
import _ from "lodash";
import React from "react";
import {
  Button, ButtonToolbar, ControlLabel,
  FormControl, FormControlProps, FormGroup,
  Row,
} from "react-bootstrap";
/**
 * Disabling here is necessary because
 * there are currently no available type definitions for
 * neither this nor any other 3rd-party react phone input components
 */
// @ts-ignore
import ReactPhoneInput from "react-phone-input-2";
import {
  ConfigProps, DecoratedComponentClass, Field,
  FormProps, formValueSelector, InjectedFormProps,
  reduxForm, WrappedFieldProps,
} from "redux-form";
import { default as Modal } from "../../../../../components/Modal/index";
import store from "../../../../../store/index";
import { msgError } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { required, validEmail } from "../../../../../utils/validations";
import Xhr from "../../../../../utils/xhr";
import * as actions from "../../../actions";
import style from "./index.css";

export interface IAddUserModalProps {
  open: boolean;
  projectName: string;
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

const phoneNumberField: ((arg1: CustomFieldProps) => JSX.Element) =
  (fieldProps: CustomFieldProps): JSX.Element => (
    <ReactPhoneInput
      defaultCountry="co"
      inputClass="form-control"
      inputStyle={{ paddingLeft: "48px" }}
      inputExtraProps={{ type: "" }}
      onChange={fieldProps.input.onChange}
      value={fieldProps.input.value}
      {...fieldProps}
    />
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

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
  }
};

const renderManagerRoles: JSX.Element = (
  <React.Fragment>
    <option value="customer">{translate.t("search_findings.tab_users.customer")}</option>
    <option value="customeradmin">{translate.t("search_findings.tab_users.customer_admin")}</option>
  </React.Fragment>
);

const renderAllRoles: JSX.Element = (
  <React.Fragment>
    <option value="analyst">{translate.t("search_findings.tab_users.analyst")}</option>
    <option value="admin">{translate.t("search_findings.tab_users.admin")}</option>
    {renderManagerRoles}
  </React.Fragment>
);

const requiredIndicator: JSX.Element = <label style={{ color: "#f22"}}>* </label>;

const renderFormContent: ((arg1: CustomFormProps) => JSX.Element) =
  (props: CustomFormProps): JSX.Element => (
  <form onSubmit={props.handleSubmit}>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {translate.t("search_findings.tab_users.textbox")}
      </ControlLabel>
      <Field
        name="email"
        component={formTextField}
        type="text"
        placeholder={translate.t("search_findings.tab_users.email")}
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
        {translate.t("search_findings.tab_users.user_organization")}
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
        {translate.t("search_findings.tab_users.role")}
      </ControlLabel>
      <Field
        name="role"
        component={formDropdownField}
        validate={[required]}
      >
        <option value="" selected={true}/>
        {props.userRole === "admin" ? renderAllRoles : undefined}
        {props.userRole === "customeradmin" ? renderManagerRoles : undefined}
      </Field>
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {translate.t("search_findings.tab_users.user_responsibility")}
      </ControlLabel>
      <Field
        name="responsability"
        component={formTextField}
        type="text"
        placeholder={translate.t("search_findings.tab_users.responsibility_placeholder")}
        validate={[required]}
      />
    </FormGroup>
    <FormGroup>
      <ControlLabel>
        {requiredIndicator}
        {translate.t("search_findings.tab_users.phone_number")}
      </ControlLabel>
      <Field
        name="phone"
        component={phoneNumberField}
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
          {translate.t("confirmmodal.cancel")}
        </Button>
        <Button
          bsStyle="primary"
          type="submit"
          disabled={props.pristine || props.submitting}
        >
          {translate.t("confirmmodal.proceed")}
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
    const title: string = props.type === "add"
    ? translate.t("search_findings.tab_users.title")
    : translate.t("search_findings.tab_users.edit_user_title");

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
