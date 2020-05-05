/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { useApolloClient } from "@apollo/react-hooks";
import ApolloClient, { ApolloError, ApolloQueryResult } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { useSelector } from "react-redux";
import { Field, formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../../components/Button/index";
import { Modal } from "../../../../../components/Modal/index";
import { Can } from "../../../../../utils/authz/Can";
import { handleErrors } from "../../../../../utils/formatHelpers";
import { dropdownField, phoneNumberField, textField } from "../../../../../utils/forms/fields";
import { msgError } from "../../../../../utils/notifications";
import translate from "../../../../../utils/translations/translate";
import { required, validAlphanumericSpace, validEmail } from "../../../../../utils/validations";
import { GenericForm } from "../../../components/GenericForm/index";
import { GET_USER } from "./queries";
import { IAddUserModalProps, IUserDataAttr } from "./types";

const requiredIndicator: JSX.Element = <label style={{ color: "#f22" }}>* </label>;

export const addUserModal: React.FC<IAddUserModalProps> = (props: IAddUserModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;
  let title: string = props.type === "add"
    ? translate.t("search_findings.tab_users.title")
    : translate.t("search_findings.tab_users.edit_user_title");
  title = props.projectName === undefined ? translate.t("sidebar.user") : title;
  const adminOption: JSX.Element | undefined = props.projectName === undefined ?
    <option value="ADMIN">{translate.t("search_findings.tab_users.admin")}</option> :
    undefined;
  const selector: (state: {}, ...field: string[]) => string = formValueSelector("addUser");
  const userEmail: string = useSelector((state: {}) => selector(state, "email"));

  const client: ApolloClient<object> = useApolloClient();

  return (
    <React.StrictMode>
      <Modal open={props.open} headerTitle={title} footer={<div />}>
        <GenericForm name="addUser" initialValues={props.initialValues} onSubmit={onSubmit}>
          {({ change }: InjectedFormProps): React.ReactNode => {
            const loadAutofillData: (() => void) = (): void => {
              if (!_.isEmpty(userEmail)) {
                client.query({
                  query: GET_USER,
                  variables: {
                    projectName: _.get(props, "projectName", "-"),
                    userEmail,
                  },
                })
                  .then(({ data, errors }: ApolloQueryResult<IUserDataAttr>) => {

                    if (!_.isUndefined(errors)) {
                      handleErrors("An error occurred getting user information for autofill", errors);
                    }
                    if (!_.isUndefined(data)) {
                      change("organization", data.user.organization);
                      change("phoneNumber", data.user.phoneNumber);
                      change("responsibility", data.user.responsibility);
                    }
                  })
                  .catch((errors: ApolloError) => {
                    errors.graphQLErrors.forEach(({ message }: GraphQLError): void => {
                      if (message !== "Exception - User not Found") {
                        msgError("An error occurred getting user information for autofill");
                      }
                    });
                  });
              }
            };

            return (
              <Row>
                <Col md={12} sm={12}>
                  <FormGroup>
                    <ControlLabel>{requiredIndicator}{translate.t("search_findings.tab_users.textbox")}</ControlLabel>
                    <Field
                      name="email"
                      component={textField}
                      type="text"
                      placeholder={translate.t("search_findings.tab_users.email")}
                      validate={[required, validEmail]}
                      disabled={props.type === "edit"}
                      onBlur={loadAutofillData}
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
                      validate={[required, validAlphanumericSpace]}
                    />
                  </FormGroup>
                  <FormGroup>
                    <ControlLabel>{requiredIndicator}{translate.t("search_findings.tab_users.role")}</ControlLabel>
                    <Field name="role" component={dropdownField} validate={[required]}>
                      <option value="" />
                      <Can do="backend_api_resolvers_user__do_grant_user_access_internal_roles">
                        <option value="ANALYST">{translate.t("search_findings.tab_users.analyst")}</option>
                        {adminOption}
                      </Can>
                      <option value="CUSTOMER">{translate.t("search_findings.tab_users.customer")}</option>
                      {props.projectName !== undefined ? (
                        <option value="CUSTOMERADMIN">
                          {translate.t("search_findings.tab_users.customeradmin")}
                        </option>
                      ) : (
                        <option value="INTERNAL_MANAGER">
                          {translate.t("search_findings.tab_users.internal_manager")}
                        </option>
                      )}
                    </Field>
                  </FormGroup>
                  {props.projectName !== undefined ? (
                    <FormGroup>
                      <ControlLabel>
                        {requiredIndicator}
                        {translate.t("search_findings.tab_users.user_responsibility")}
                      </ControlLabel>
                      <Field
                        name="responsibility"
                        component={textField}
                        type="text"
                        placeholder={translate.t("search_findings.tab_users.responsibility_placeholder")}
                        validate={[required]}
                      />
                    </FormGroup>
                  ) : undefined}
                  <FormGroup>
                    <ControlLabel>{translate.t("search_findings.tab_users.phone_number")}</ControlLabel>
                    <Field name="phoneNumber" component={phoneNumberField} type="text" />
                  </FormGroup>
                </Col>
                <Col md={12} sm={12}>
                  <ButtonToolbar className="pull-right">
                    <Button bsStyle="default" onClick={onClose}>{translate.t("confirmmodal.cancel")}</Button>
                    <Button bsStyle="primary" type="submit">{translate.t("confirmmodal.proceed")}</Button>
                  </ButtonToolbar>
                </Col>
              </Row>
            );
          }}
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};
