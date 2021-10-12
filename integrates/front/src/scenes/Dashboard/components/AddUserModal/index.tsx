import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Field, Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { object, string } from "yup";

import { getNewInitialValues, getUserData } from "./helpers";

import { Button } from "components/Button/index";
import { Modal } from "components/Modal";
import { GET_STAKEHOLDER } from "scenes/Dashboard/components/AddUserModal/queries";
import type {
  IAddStakeholderModalProps,
  IStakeholderAttrs,
} from "scenes/Dashboard/components/AddUserModal/types";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  FormGroup,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { FormikDropdown, FormikText } from "utils/forms/fields";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { validTextField } from "utils/validations";

const userLevelRoles: string[] = ["admin", "customer", "hacker"];
const groupLevelRoles: string[] = [
  "customer",
  "customeradmin",
  "executive",
  "hacker",
  "reattacker",
  "resourcer",
  "reviewer",
  "system_owner",
];
const organizationLevelRoles: string[] = [
  "customeradmin",
  "customer",
  "system_owner",
];
const MAX_RESPONSIBILITY_LENGTH: number = 50;

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
    groupName,
    title,
    type,
  } = props;
  const newTitle: string = action === "add" ? title : editTitle;
  const groupModal: boolean = groupName !== undefined;
  const organizationModal: boolean = type === "organization";
  const sidebarModal: boolean = type === "user" && groupName === undefined;
  const newInitialValues: Record<string, string> = getNewInitialValues(
    initialValues,
    action,
    organizationModal
  );

  const [getUser, { data }] = useLazyQuery<IStakeholderAttrs>(GET_STAKEHOLDER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message !== "Access denied or stakeholder not found") {
          msgError(translate.t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred getting user information for autofill",
            error
          );
        }
      });
    },
  });

  function loadAutofillData(event: React.FocusEvent<HTMLInputElement>): void {
    const userEmail: string = event.target.value;
    if (!_.isEmpty(userEmail)) {
      getUser({
        variables: {
          entity: organizationModal ? "ORGANIZATION" : "GROUP",
          groupName: _.get(props, "groupName", "-"),
          organizationId: _.get(props, "organizationId", "-"),
          userEmail,
        },
      });
    }
  }

  const userData = getUserData(data);

  const addUserModalSchema = object().shape({
    email: string()
      .email(translate.t("validations.email"))
      .required(translate.t("validations.required")),
    responsibility: string()
      .when("$groupName", {
        is: groupName,
        otherwise: string().required(translate.t("validations.required")),
        then: string(),
      })
      .max(
        MAX_RESPONSIBILITY_LENGTH,
        translate.t("validations.maxLength", {
          count: MAX_RESPONSIBILITY_LENGTH,
        })
      ),
    /*
     * The forbidden characters (e.g. =,'',"") check
     * will still be performed by the old custom
     * method via field-level validation
     */
    role: string().required(translate.t("validations.required")),
  });

  return (
    <React.StrictMode>
      <Modal headerTitle={newTitle} onEsc={onClose} open={open}>
        <Formik
          context={{ groupName }}
          enableReinitialize={true}
          initialValues={{ ...newInitialValues, ...userData }}
          name={"addUser"}
          onSubmit={onSubmit}
          validationSchema={addUserModalSchema}
        >
          <Form>
            <Row>
              <Col100>
                <FormGroup>
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("userModal.emailText")}
                  </ControlLabel>
                  <Field
                    component={FormikText}
                    customBlur={loadAutofillData}
                    disabled={action === "edit"}
                    name={"email"}
                    placeholder={translate.t("userModal.emailPlaceholder")}
                    type={"text"}
                  />
                </FormGroup>
                <FormGroup>
                  <ControlLabel>
                    <RequiredField>{"* "}</RequiredField>
                    {translate.t("userModal.role")}
                  </ControlLabel>
                  <Field component={FormikDropdown} name={"role"}>
                    <option value={""} />
                    {(groupModal ? groupLevelRoles : []).map(
                      (role: string): JSX.Element => (
                        <Can do={`grant_group_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {translate.t(
                              `userModal.roles.${_.camelCase(role)}`
                            )}
                          </option>
                        </Can>
                      )
                    )}
                    {(sidebarModal ? userLevelRoles : []).map(
                      (role: string): JSX.Element => (
                        <Can do={`grant_user_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {translate.t(
                              `userModal.roles.${_.camelCase(role)}`
                            )}
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
                {groupName === undefined ? undefined : (
                  <FormGroup>
                    <ControlLabel>
                      <RequiredField>{"* "}</RequiredField>
                      {translate.t("userModal.responsibility")}
                    </ControlLabel>
                    <Field
                      component={FormikText}
                      name={"responsibility"}
                      placeholder={translate.t(
                        "userModal.responsibilityPlaceholder"
                      )}
                      type={"text"}
                      validate={validTextField}
                    />
                  </FormGroup>
                )}
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
          </Form>
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};
