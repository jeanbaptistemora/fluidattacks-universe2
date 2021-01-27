import type { ApolloError } from "apollo-client";
import { Button } from "components/Button/index";
import { Can } from "utils/authz/Can";
import { Field } from "redux-form";
import { GET_USER } from "scenes/Dashboard/components/AddUserModal/queries";
import { GenericForm } from "scenes/Dashboard/components/GenericForm";
import type { GraphQLError } from "graphql";
import { Logger } from "utils/logger";
import { Modal } from "components/Modal";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useLazyQuery } from "@apollo/react-hooks";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Dropdown, PhoneNumber, Text } from "utils/forms/fields";
import type {
  IAddStakeholderModalProps,
  IStakeholderAttrs,
} from "scenes/Dashboard/components/AddUserModal/types";
import { required, validEmail, validTextField } from "utils/validations";

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
            msgError(translate.t("group_alerts.error_textsad"));
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
                          {translate.t(`userModal.roles.${role}`)}
                        </option>
                      </Can>
                    )
                  )}
                  {(sidebarModal ? userLevelRoles : []).map(
                    (role: string): JSX.Element => (
                      <Can do={`grant_user_level_role:${role}`} key={role}>
                        <option value={role.toUpperCase()}>
                          {translate.t(`userModal.roles.${role}`)}
                        </option>
                      </Can>
                    )
                  )}
                  {(organizationModal ? organizationLevelRoles : []).map(
                    (role: string): JSX.Element => (
                      <option key={role} value={role.toUpperCase()}>
                        {translate.t(`userModal.roles.${role}`)}
                      </option>
                    )
                  )}
                </Field>
              </FormGroup>
              {projectName !== undefined ? (
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
                    validate={[required, validTextField]}
                  />
                </FormGroup>
              ) : undefined}
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
