import { useLazyQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Form, Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { StrictMode, useEffect, useState } from "react";
import type { FC, FocusEvent } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { GET_STAKEHOLDER } from "./queries";
import type { IUserAttrs } from "./types";

import { DataList, Input, Select } from "components/Input";
import { Gap } from "components/Layout";
import { Modal, ModalConfirm } from "components/Modal";
import { Can } from "utils/authz/Can";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { validTextField } from "utils/validations";

interface IAddUserModalProps {
  action: "add" | "edit";
  editTitle: string;
  initialValues?: Record<string, string>;
  open: boolean;
  organizationId?: string;
  groupName?: string;
  domainSuggestings: string[];
  suggestions: string[];
  title: string;
  type: "organization" | "user";
  onClose: () => void;
  // Annotation needed for compatibility with Group and Organization
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onSubmit: (values: any) => void;
}

const getUserData = (data: IUserAttrs | undefined): Record<string, string> =>
  _.isEmpty(data) || _.isUndefined(data) ? {} : data.stakeholder;

const getNewInitialValues = (
  initialValues: Record<string, string>,
  action: string,
  organizationModal: boolean
): Record<string, string> =>
  action === "edit"
    ? {
        email: initialValues.email,
        responsibility: organizationModal ? "" : initialValues.responsibility,
        role: initialValues.role.toUpperCase(),
      }
    : {};

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

const AddUserModal: FC<IAddUserModalProps> = ({
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
}: Readonly<IAddUserModalProps>): JSX.Element => {
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

  const [getUser, { data }] = useLazyQuery<IUserAttrs>(GET_STAKEHOLDER, {
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

  function loadAutofillData(event: FocusEvent<HTMLInputElement>): void {
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

  const listGroupRoles: JSX.Element[] = (groupModal ? groupLevelRoles : []).map(
    (role: string): JSX.Element => (
      <Can do={`grant_group_level_role:${role}`} key={role}>
        <option value={role.toUpperCase()}>
          {t(`userModal.roles.${_.camelCase(role)}`)}
        </option>
      </Can>
    )
  );

  const listOrgRoles: JSX.Element[] = (
    isOrganizationTypeModal ? organizationLevelRoles : []
  ).map(
    (role: string): JSX.Element => (
      <option key={role} value={role.toUpperCase()}>
        {t(`userModal.roles.${_.camelCase(role)}`)}
      </option>
    )
  );

  useEffect((): void => {
    setUserSuggestions(suggestions);
  }, [suggestions]);

  return (
    <StrictMode>
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
                    label={t("userModal.emailText")}
                    list={"email-datalist"}
                    name={"email"}
                    onBlur={
                      isOrganizationTypeModal ? undefined : loadAutofillData
                    }
                    placeholder={t("userModal.emailPlaceholder")}
                    required={true}
                    type={"email"}
                  />
                  <DataList data={userSuggestions} id={"email-datalist"} />
                  <Select
                    label={t("userModal.role")}
                    name={"role"}
                    required={true}
                  >
                    <option value={""} />
                    {listGroupRoles}
                    {(sidebarModal ? userLevelRoles : []).map(
                      (role: string): JSX.Element => (
                        <Can do={`grant_user_level_role:${role}`} key={role}>
                          <option value={role.toUpperCase()}>
                            {t(`userModal.roles.${_.camelCase(role)}`)}
                          </option>
                        </Can>
                      )
                    )}
                    {listOrgRoles}
                  </Select>
                  {groupName === undefined ? undefined : (
                    <Input
                      label={t("userModal.responsibility")}
                      name={"responsibility"}
                      placeholder={t("userModal.responsibilityPlaceholder")}
                      required={true}
                      validate={validTextField}
                    />
                  )}
                </Gap>
                <ModalConfirm onCancel={onClose} />
              </Form>
            );
          }}
        </Formik>
      </Modal>
    </StrictMode>
  );
};

export { AddUserModal };
