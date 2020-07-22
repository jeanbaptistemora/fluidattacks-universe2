/* tslint:disable:jsx-no-multiline-js
 *
 * NO-MULTILINE-JS: Disabling this rule is necessary for the sake of
  * readability of the code that defines the headers of the table
 */
import { useLazyQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { ButtonToolbar, Col, ControlLabel, FormGroup, Row } from "react-bootstrap";
import { Field } from "redux-form";
import { Button } from "../../../../components/Button/index";
import { Modal } from "../../../../components/Modal/index";
import { Can } from "../../../../utils/authz/Can";
import { Dropdown, PhoneNumber, Text } from "../../../../utils/forms/fields";
import { msgError } from "../../../../utils/notifications";
import rollbar from "../../../../utils/rollbar";
import translate from "../../../../utils/translations/translate";
import { required, validAlphanumericSpace, validEmail, validTextField } from "../../../../utils/validations";
import { GenericForm } from "../GenericForm/index";
import { GET_USER } from "./queries";
import { IAddUserModalProps, IUserDataAttr } from "./types";

const requiredIndicator: JSX.Element = <label style={{ color: "#f22" }}>* </label>;
const userLevelRoles: string[] = [
  "admin",
  "customer",
  "internal_manager",
];
const groupLevelRoles: string[] = [
  "analyst",
  "closer",
  "customer",
  "customeradmin",
  "executive",
  "group_manager",
  "resourcer",
  "reviewer",
];
const organizationLevelRoles: string[] = [
  "customeradmin",
  "customer",
];

export const addUserModal: React.FC<IAddUserModalProps> = (props: IAddUserModalProps): JSX.Element => {
  const { onClose, onSubmit } = props;
  const title: string = props.action === "add"
      ? props.title
      : props.editTitle;

  const [getUser, { data }] = useLazyQuery<IUserDataAttr>(GET_USER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
        rollbar.error(
          "An error occurred getting user information for autofill",
          error,
        );
      });
    },
  });

  const userData: Record<string, string> =
    _.isEmpty(data) || _.isUndefined(data) ? {} : data.user;

  const loadAutofillData: ((event: React.FocusEvent<HTMLInputElement>) => void) = (
    event: React.FocusEvent<HTMLInputElement>,
  ): void => {
    const userEmail: string = event.target.value;
    if (!_.isEmpty(userEmail)) {
      getUser({
        variables: {
          entity: organizationModal
                  ? "ORGANIZATION"
                  : "PROJECT",
          organizationId: _.get(props, "organizationId", "-"),
          projectName: _.get(props, "projectName", "-"),
          userEmail,
        },
      });
    }
  };

  const initialValues: Record<string, string> = props.action === "edit"
    ? {
        ...props.initialValues,
        role: props.initialValues.role.toUpperCase(),
      }
    : {};

  const groupModal: boolean = props.projectName !== undefined;
  const organizationModal: boolean = props.type === "organization";
  const sidebarModal: boolean = props.type === "user" && props.projectName === undefined;

  return (
    <React.StrictMode>
      <Modal open={props.open} headerTitle={title} footer={<div />}>
        <GenericForm
          name="addUser"
          initialValues={{...initialValues, ...userData }}
          onSubmit={onSubmit}
        >
          <Row>
            <Col md={12} sm={12}>
              <FormGroup>
                <ControlLabel>{requiredIndicator}{translate.t("userModal.emailText")}</ControlLabel>
                <Field
                  name="email"
                  component={Text}
                  type="text"
                  placeholder={translate.t("userModal.emailPlaceholder")}
                  validate={[required, validEmail]}
                  disabled={props.action === "edit"}
                  onBlur={loadAutofillData}
                />
              </FormGroup>
              <FormGroup>
                <ControlLabel>{requiredIndicator}{translate.t("userModal.role")}</ControlLabel>
                <Field name="role" component={Dropdown} validate={[required]}>
                  <option value="" />
                  {(groupModal ? groupLevelRoles : []).map((role: string) => (
                    <Can do={`grant_group_level_role:${role}`} key={role}>
                      <option value={role.toUpperCase()}>
                        {translate.t(`userModal.roles.${role}`)}
                      </option>
                    </Can>
                  ))}
                  {(sidebarModal ? userLevelRoles : []).map((role: string) => (
                    <Can do={`grant_user_level_role:${role}`} key={role}>
                      <option value={role.toUpperCase()}>
                        {translate.t(`userModal.roles.${role}`)}
                      </option>
                    </Can>
                  ))}
                  {(organizationModal ? organizationLevelRoles : []).map((role: string) => (
                    <option value={role.toUpperCase()} key={role}>
                      {translate.t(`userModal.roles.${role}`)}
                    </option>
                  ))}
                </Field>
              </FormGroup>
              {props.projectName !== undefined ? (
                <FormGroup>
                  <ControlLabel>
                    {requiredIndicator}
                    {translate.t("userModal.responsibility")}
                  </ControlLabel>
                  <Field
                    name="responsibility"
                    component={Text}
                    type="text"
                    placeholder={translate.t("userModal.responsibilityPlaceholder")}
                    validate={[required, validTextField]}
                  />
                </FormGroup>
              ) : undefined}
              <FormGroup>
                <ControlLabel>{translate.t("userModal.phoneNumber")}</ControlLabel>
                <Field name="phoneNumber" component={PhoneNumber} type="text" />
              </FormGroup>
            </Col>
            <Col md={12} sm={12}>
              <ButtonToolbar className="pull-right">
                <Button bsStyle="default" onClick={onClose}>{translate.t("confirmmodal.cancel")}</Button>
                <Button bsStyle="primary" type="submit">{translate.t("confirmmodal.proceed")}</Button>
              </ButtonToolbar>
            </Col>
          </Row>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};
