import { AxiosError, AxiosResponse } from "axios";
import _ from "lodash";
import React from "react";
import {
  Button, ButtonToolbar, ControlLabel, FormGroup,
  Row,
} from "react-bootstrap";
import {
  ConfigProps, DecoratedComponentClass, Field, formValueSelector, InjectedFormProps,
  reduxForm,
} from "redux-form";
import { default as Modal } from "../../../../../components/Modal/index";
import store from "../../../../../store/index";
import { dropdownField, phoneNumberField, textField } from "../../../../../utils/forms/fields";
import { msgError } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { required, validEmail } from "../../../../../utils/validations";
import Xhr from "../../../../../utils/xhr";
import * as actions from "../actions";

export interface IAddUserModalProps {
  open: boolean;
  projectName: string;
  type: "add" | "edit";
  userRole: string;
}

type CustomFormProps = IAddUserModalProps & InjectedFormProps<{}, IAddUserModalProps>;

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
        component={textField}
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
        component={textField}
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
        component={dropdownField}
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
        component={textField}
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
