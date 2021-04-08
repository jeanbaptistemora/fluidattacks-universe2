import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Field } from "redux-form";
import type { ConfigurableValidator } from "revalidate";

import { Button } from "components/Button/index";
import { Modal } from "components/Modal";
import { GET_USER } from "scenes/Dashboard/components/AddUserModal/queries";
import type {
  IAddStakeholderModalProps,
  IStakeholderAttrs,
} from "scenes/Dashboard/components/AddUserModal/types";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Dropdown, PhoneNumber, Text } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import {
  maxLength,
  required,
  validEmail,
  validTextField,
} from "utils/validations";

const userLevelRoles: string[] = ["admin", "customer", "analyst"];
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
  "group_manager",
];
const MAX_RESPONSIBILITY_LENGTH: number = 50;
const maxResponsibilityLength: ConfigurableValidator = maxLength(
  MAX_RESPONSIBILITY_LENGTH
);

export const AddUserModal: React.FC<IAddStakeholderModalProps> = (
  props: IAddStakeholderModalProps
): JSX.Element => {
  const {
    action,
    editTitle,
    initialValues,
    onClose,
    onSubmit,
    open,
    projectName,
    title,
    type,
  } = props;
  const newTitle: string = action === "add" ? title : editTitle;
  const groupModal: boolean = projectName !== undefined;
  const organizationModal: boolean = type === "organization";
  const sidebarModal: boolean = type === "user" && projectName === undefined;
  const newInitialValues: Record<string, string> =
    action === "edit"
      ? {
          email: initialValues.email,
          phoneNumber: initialValues.phoneNumber,
          responsibility: organizationModal ? "" : initialValues.responsibility,
          role: initialValues.role.toUpperCase(),
        }
      : {};

  const [getUser, { data }] = useLazyQuery<IStakeholderAttrs>(GET_USER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Access denied or stakeholder not found":
            break;
          default:
            msgError(translate.t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred getting user information for autofill",
              error
            );
        }
      });
    },
  });

  const userData: Record<string, string> =
    _.isEmpty(data) || _.isUndefined(data) ? {} : data.stakeholder;

  function loadAutofillData(event: React.FocusEvent<HTMLInputElement>): void {
    const userEmail: string = event.target.value;
    if (!_.isEmpty(userEmail)) {
      getUser({
        variables: {
          entity: organizationModal ? "ORGANIZATION" : "PROJECT",
          organizationId: _.get(props, "organizationId", "-"),
          projectName: _.get(props, "projectName", "-"),
          userEmail,
        },
      });
    }
  }

  return (
    <React.StrictMode>
      <Modal headerTitle={newTitle} open={open}>
        <GenericForm
          initialValues={{ ...newInitialValues, ...userData }}
          name={"addUser"}
          onSubmit={onSubmit}
        >
          <Row>
            <Col100>
              <FormGroup>
                <ControlLabel>
                  <RequiredField>{"* "}</RequiredField>
                  {translate.t("userModal.emailText")}
                </ControlLabel>
                <Field
                  component={Text}
                  disabled={action === "edit"}
                  name={"email"}
                  onBlur={loadAutofillData}
                  placeholder={translate.t("userModal.emailPlaceholder")}
                  type={"text"}
                  validate={[required, validEmail]}
                />
              </FormGroup>
              <FormGroup>
                <ControlLabel>
                  <RequiredField>{"* "}</RequiredField>
                  {translate.t("userModal.role")}
                </ControlLabel>
                <Field component={Dropdown} name={"role"} validate={[required]}>
                  <option value={""} />
                  {(groupModal ? groupLevelRoles : []).map(
                    (role: string): JSX.Element => (
                      <Can do={`grant_group_level_role:${role}`} key={role}>
                        <option value={role.toUpperCase()}>
                          {translate.t(`userModal.roles.${_.camelCase(role)}`)}
                        </option>
                      </Can>
                    )
                  )}
                  {(sidebarModal ? userLevelRoles : []).map(
                    (role: string): JSX.Element => (
                      <Can do={`grant_user_level_role:${role}`} key={role}>
                        <option value={role.toUpperCase()}>
                          {translate.t(`userModal.roles.${_.camelCase(role)}`)}
                        </option>
                      </Can>
                    )
                  )}
                  {(organizationModal ? organizationLevelRoles : []).map(
                    (role: string): JSX.Element => (
                      <option key={role} value={role.toUpperCase()}>
                        {translate.t(`userModal.roles.${_.camelCase(role)}`)}
                      </option>
                    )
                  )}
                </Field>
              </FormGroup>
              {projectName === undefined ? undefined : (
                <FormGroup>
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("userModal.responsibility")}
                  </ControlLabel>
                  <Field
                    component={Text}
                    name={"responsibility"}
                    placeholder={translate.t(
                      "userModal.responsibilityPlaceholder"
                    )}
                    type={"text"}
                    validate={[
                      maxResponsibilityLength,
                      required,
                      validTextField,
                    ]}
                  />
                </FormGroup>
              )}
              <FormGroup>
                <ControlLabel>
                  {translate.t("userModal.phoneNumber")}
                </ControlLabel>
                <Field
                  component={PhoneNumber}
                  name={"phoneNumber"}
                  type={"text"}
                />
              </FormGroup>
            </Col100>
          </Row>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={onClose}>
                  {translate.t("confirmmodal.cancel")}
                </Button>
                <Button type={"submit"}>
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </GenericForm>
      </Modal>
    </React.StrictMode>
  );
};
