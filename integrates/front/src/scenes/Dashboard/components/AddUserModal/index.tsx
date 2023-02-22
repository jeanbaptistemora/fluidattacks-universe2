import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { getNewInitialValues, getUserData } from "./helpers";

import { DataList, Input, Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { GET_STAKEHOLDER } from "scenes/Dashboard/components/AddUserModal/queries";
import type {
  IAddStakeholderModalProps,
  IStakeholderAttrs,
} from "scenes/Dashboard/components/AddUserModal/types";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { validTextField } from "utils/validations";

const userLevelRoles: string[] = ["user", "hacker", "admin"];
const groupLevelRoles: string[] = [
  "user",
  "user_manager",
  "customer_manager",
  "vulnerability_manager",
  "architect",
  "hacker",
  "reattacker",
  "resourcer",
  "reviewer",
];
const organizationLevelRoles: string[] = [
  "user",
  "user_manager",
  "customer_manager",
];
const MAX_RESPONSIBILITY_LENGTH: number = 50;

export const AddUserModal: React.FC<IAddStakeholderModalProps> = ({
  action,
  editTitle,
  initialValues,
  onClose,
  onSubmit,
  open,
  organizationId,
  groupName,
  domainSuggestings,
  suggestions,
  title,
  type,
}: IAddStakeholderModalProps): JSX.Element => {
  const { t } = useTranslation();
  const newTitle: string = action === "add" ? title : editTitle;
  const groupModal: boolean = groupName !== undefined;
  const isOrganizationTypeModal: boolean = type === "organization";
  const sidebarModal: boolean = type === "user" && groupName === undefined;
  const newInitialValues: Record<string, string> = getNewInitialValues(
    _.isEmpty(initialValues) || initialValues === undefined
      ? { email: "", organizationModal: "", role: "" }
      : initialValues,
    action,
    isOrganizationTypeModal
  );
  const [userSuggestions, setUserSuggestions] = useState(suggestions);

  const [getUser, { data }] = useLazyQuery<IStakeholderAttrs>(GET_STAKEHOLDER, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        if (error.message !== "Access denied or stakeholder not found") {
          msgError(t("groupAlerts.errorTextsad"));
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
          entity: isOrganizationTypeModal ? "ORGANIZATION" : "GROUP",
          groupName: groupName ?? "-",
          organizationId: organizationId ?? "-",
          userEmail,
        },
      });
    }
  }

  const userData = getUserData(data);

  const addUserModalSchema = object().shape({
    email: string()
      .email(t("validations.email"))
      .required(t("validations.required")),
    responsibility: string()
      .when("$groupName", {
        is: groupName,
        otherwise: string().required(t("validations.required")),
        then: string(),
      })
      .max(
        MAX_RESPONSIBILITY_LENGTH,
        t("validations.maxLength", {
          count: MAX_RESPONSIBILITY_LENGTH,
        })
      ),
    /*
     * The forbidden characters (e.g. =,'',"") check
     * will still be performed by the old custom
     * method via field-level validation
     */
    role: string().required(t("validations.required")),
  });

  const groupRoles: string[] = groupModal ? groupLevelRoles : [];
  const userRoles: string[] = sidebarModal ? userLevelRoles : [];
  const organizationRoles: string[] = isOrganizationTypeModal
    ? organizationLevelRoles
    : [];

  useEffect((): void => {
    setUserSuggestions(suggestions);
  }, [suggestions]);

  return (
    <React.StrictMode>
      <Modal onClose={onClose} open={open} title={newTitle}>
        <Formik
          context={{ groupName }}
          enableReinitialize={true}
          initialValues={{ ...newInitialValues, ...userData }}
          name={"addUser"}
          onSubmit={onSubmit}
          validationSchema={addUserModalSchema}
        >
          {({ values }): JSX.Element => {
            const { email: currentEmail } = values;

            if (
              // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
              currentEmail !== undefined
            ) {
              if (currentEmail.length > 1 && currentEmail.endsWith("@")) {
                const domainUser = domainSuggestings.map(
                  (domain: string): string => `${currentEmail}${domain}`
                );
                const isNotInList =
                  domainUser.filter(
                    (domainEmail: string): boolean =>
                      !userSuggestions.includes(domainEmail)
                  ).length > 0;
                if (isNotInList) {
                  setUserSuggestions((): string[] => {
                    return Array.from(new Set([...suggestions, ...domainUser]));
                  });
                }
              } else if (currentEmail === "" || !currentEmail.includes("@")) {
                if (userSuggestions.length !== suggestions.length) {
                  setUserSuggestions(suggestions);
                }
              }
            }

            return (
              <Form>
                <Gap disp={"block"} mv={12}>
                  <Input
                    disabled={action === "edit"}
                    label={
                      <Fragment>
                        <Text disp={"inline"} tone={"red"}>
                          {"* "}
                        </Text>
                        {t("userModal.emailText")}
                      </Fragment>
                    }
                    list={"email-datalist"}
                    name={"email"}
                    onBlur={
                      isOrganizationTypeModal ? undefined : loadAutofillData
                    }
                    placeholder={t("userModal.emailPlaceholder")}
                    type={"email"}
                  />
                  <DataList data={userSuggestions} id={"email-datalist"} />
                  <Select
                    label={
                      <Fragment>
                        <Text disp={"inline"} tone={"red"}>
                          {"* "}
                        </Text>
                        {t("userModal.role")}
                      </Fragment>
                    }
                    name={"role"}
                  >
                    <option value={""} />
                    {groupRoles.map(
                      (role: string): JSX.Element => (
                        <Can do={`grant_group_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {t(`userModal.roles.${_.camelCase(role)}`)}
                          </option>
                        </Can>
                      )
                    )}
                    {userRoles.map(
                      (role: string): JSX.Element => (
                        <Can do={`grant_user_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {t(`userModal.roles.${_.camelCase(role)}`)}
                          </option>
                        </Can>
                      )
                    )}
                    {organizationRoles.map(
                      (role: string): JSX.Element => (
                        <option key={role} value={role.toUpperCase()}>
                          {t(`userModal.roles.${_.camelCase(role)}`)}
                        </option>
                      )
                    )}
                  </Select>
                  {groupName === undefined ? undefined : (
                    <Fragment>
                      <Text mb={1}>
                        <Text disp={"inline"} tone={"red"}>
                          {"* "}
                        </Text>
                        {t("userModal.responsibility")}
                      </Text>
                      <Input
                        name={"responsibility"}
                        placeholder={t("userModal.responsibilityPlaceholder")}
                        type={"text"}
                        validate={validTextField}
                      />
                    </Fragment>
                  )}
                </Gap>
                <ModalConfirm onCancel={onClose} />
              </Form>
            );
          }}
        </Formik>
      </Modal>
    </React.StrictMode>
  );
};
