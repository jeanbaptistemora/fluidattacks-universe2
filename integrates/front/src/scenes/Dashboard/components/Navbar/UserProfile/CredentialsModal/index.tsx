import { Buffer } from "buffer";

import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { FormikHelpers } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "./ActionButtons";
import { CredentialsForm } from "./CredentialsForm";
import type { IFormValues } from "./CredentialsForm/types";
import {
  ADD_CREDENTIALS,
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
  REMOVE_CREDENTIALS,
  UPDATE_CREDENTIALS,
} from "./queries";
import type {
  IAddCredentialsResultAttr,
  ICredentialAttr,
  ICredentialData,
  ICredentialModalProps as ICredentialsModalProps,
  IOrganizationAttr,
  IRemoveCredentialsResultAttr,
  IUpdateCredentialsResultAttr,
} from "./types";

import { Modal } from "components/Modal";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { editAndDeleteActionFormatter } from "scenes/Dashboard/components/Navbar/UserProfile/CredentialsModal/formatters/editAndDeleteActionFormatter";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const CredentialsModal: React.FC<ICredentialsModalProps> = (
  props: ICredentialsModalProps
): JSX.Element => {
  const { isOpen, onClose } = props;
  const { t } = useTranslation();

  // States
  const [isAdding, setIsAdding] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [credentialsToEditId, setCredentialsToEditId] = useState<
    string | undefined
  >(undefined);
  const [formInitialValues, setFormInitialValues] = useState<
    IFormValues | undefined
  >(undefined);
  const [newSecrets, setNewSecrets] = useState(false);

  // GraphQl mutations
  const [handleAddCredentials] = useMutation<IAddCredentialsResultAttr>(
    ADD_CREDENTIALS,
    {
      onCompleted: (data: IAddCredentialsResultAttr): void => {
        if (data.addCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.addSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding credential", error);
          }
        });
      },
      refetchQueries: [{ query: GET_STAKEHOLDER_CREDENTIALS }],
    }
  );
  const [handleRemoveCredentials] = useMutation<IRemoveCredentialsResultAttr>(
    REMOVE_CREDENTIALS,
    {
      onCompleted: (data: IRemoveCredentialsResultAttr): void => {
        if (data.removeCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.removeSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding credentials", error);
          }
        });
      },
      refetchQueries: [{ query: GET_STAKEHOLDER_CREDENTIALS }],
    }
  );
  const [handleUpdateCredentials] = useMutation<IUpdateCredentialsResultAttr>(
    UPDATE_CREDENTIALS,
    {
      onCompleted: (data: IUpdateCredentialsResultAttr): void => {
        if (data.updateCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.editSuccess"),
            t("groupAlerts.titleSuccess")
          );
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          switch (error.message) {
            case "Exception - A credential exists with the same name":
              msgError(t("validations.invalidCredentialName"));
              break;
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred editing credentials", error);
          }
        });
      },
      refetchQueries: [{ query: GET_STAKEHOLDER_CREDENTIALS }],
    }
  );

  // GraphQl queries
  const { data } = useQuery<{
    me: { credentials: ICredentialAttr[] };
  }>(GET_STAKEHOLDER_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder credentials", error);
      });
    },
  });
  const { data: organizationsData } = useQuery<{
    me: { organizations: IOrganizationAttr[] };
  }>(GET_STAKEHOLDER_ORGANIZATIONS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load stakeholder credentials", error);
      });
    },
  });

  // Format data
  const credentialsAttrs = _.isUndefined(data) ? [] : data.me.credentials;
  const credentials: ICredentialData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialAttr): ICredentialData => ({
      ...credentialAttr,
      organizationId: credentialAttr.organization.id,
      organizationName: credentialAttr.organization.name,
    })
  );

  const organizations = _.isUndefined(organizationsData)
    ? []
    : organizationsData.me.organizations;

  // Handle actions
  async function handleSubmit(
    values: IFormValues,
    { resetForm }: FormikHelpers<IFormValues>
  ): Promise<void> {
    const secrets = values.isHttpsType
      ? values.isHttpsPasswordType
        ? {
            password: values.password,
            type: "HTTPS",
            user: values.user,
          }
        : { token: values.accessToken, type: "HTTPS" }
      : {
          key: Buffer.from(
            _.isUndefined(values.sshKey) ? "" : values.sshKey
          ).toString("base64"),
          type: "SSH",
        };

    if (isAdding) {
      const addingResult = await handleAddCredentials({
        variables: {
          credentials: {
            name: values.name,
            ...secrets,
          },
          organizationId: values.organization,
        },
      });
      if (
        !_.isNil(addingResult.data) &&
        addingResult.data.addCredentials.success
      ) {
        resetForm();
        setIsAdding(false);
      }
    }

    if (isEditing) {
      const editingResult = await handleUpdateCredentials({
        variables: {
          credentials: newSecrets
            ? {
                name: values.name,
                ...secrets,
              }
            : {
                name: values.name,
              },
          credentialsId: credentialsToEditId,
          organizationId: values.organization,
        },
      });
      if (
        !_.isNil(editingResult.data) &&
        editingResult.data.updateCredentials.success
      ) {
        resetForm();
        setIsEditing(false);
        setNewSecrets(false);
      }
    }
  }
  function handleOnAdd(): void {
    setIsAdding(true);
  }
  function handleOnCancel(): void {
    setIsAdding(false);
    setIsEditing(false);
  }
  function handleOnRemove(
    credentialsToRemove: Record<string, string> | undefined
  ): void {
    if (!_.isUndefined(credentialsToRemove)) {
      void handleRemoveCredentials({
        variables: {
          credentialsId: credentialsToRemove.id,
          organizationId: credentialsToRemove.organizationId,
        },
      });
    }
  }
  function handleOnEdit(
    credentialsToEdit: Record<string, string> | undefined
  ): void {
    if (!_.isUndefined(credentialsToEdit)) {
      setFormInitialValues({
        accessToken: undefined,
        isHttpsPasswordType: true,
        isHttpsType: credentialsToEdit.type === "HTTPS",
        name: credentialsToEdit.name,
        organization: credentialsToEdit.organizationId,
        password: undefined,
        sshKey: undefined,
        user: undefined,
      });
      setCredentialsToEditId(credentialsToEdit.id);
      setIsEditing(true);
      setIsAdding(false);
    }
  }

  // Table config
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: t("profile.credentialsModal.table.columns.name"),
      wrapped: true,
    },
    {
      dataField: "type",
      header: t("profile.credentialsModal.table.columns.type"),
      wrapped: true,
    },
    {
      dataField: "organizationName",
      header: t("profile.credentialsModal.table.columns.organization"),
      wrapped: true,
    },
    {
      dataField: "id",
      deleteFunction: handleOnRemove,
      editFunction: handleOnEdit,
      formatter: editAndDeleteActionFormatter,
      header: t("profile.credentialsModal.table.columns.action"),
      width: "60px",
    },
  ];

  return (
    <Modal
      minWidth={850}
      onClose={onClose}
      open={isOpen}
      title={t("profile.credentialsModal.title")}
    >
      <CredentialsForm
        initialValues={isAdding ? undefined : formInitialValues}
        isAdding={isAdding}
        isEditing={isEditing}
        newSecrets={newSecrets}
        onCancel={handleOnCancel}
        onSubmit={handleSubmit}
        organizations={organizations}
        setNewSecrets={setNewSecrets}
      />
      {isAdding || isEditing ? undefined : (
        <Table
          dataset={credentials}
          exportCsv={false}
          extraButtonsRight={
            <ActionButtons isAdding={isAdding} onAdd={handleOnAdd} />
          }
          headers={tableHeaders}
          id={"tblCredentials"}
          pageSize={10}
          search={false}
        />
      )}
    </Modal>
  );
};

export { CredentialsModal };
