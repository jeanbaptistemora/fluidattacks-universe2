import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { FormikHelpers } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "./ActionButtons";
import { CredentialForm } from "./CredentialForm";
import type { IFormValues } from "./CredentialForm/types";
import {
  ADD_CREDENTIALS,
  GET_STAKEHOLDER_CREDENTIALS,
  GET_STAKEHOLDER_ORGANIZATIONS,
} from "./queries";
import type {
  IAddCredentialsResultAttr,
  ICredentialAttr,
  ICredentialData,
  ICredentialModalProps,
  IOrganizationAttr,
} from "./types";

import { Modal } from "components/Modal";
import { Table } from "components/Table";
import { editAndDeleteActionFormatter } from "components/Table/formatters/editAndDeleteActionFormatter";
import type { IHeaderConfig } from "components/Table/types";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const CredentialModal: React.FC<ICredentialModalProps> = (
  props: ICredentialModalProps
): JSX.Element => {
  const { isOpen, onClose } = props;
  const { t } = useTranslation();

  // States
  const [isAdding, setIsAdding] = useState(true);
  const [isEditing, setIsEditing] = useState(false);

  // GraphQl mutations
  const [handleAddCredentials] = useMutation<IAddCredentialsResultAttr>(
    ADD_CREDENTIALS,
    {
      onCompleted: (data: IAddCredentialsResultAttr): void => {
        if (data.addCredentials.success) {
          msgSuccess(
            t("profile.credentialsModal.alerts.additionSuccess"),
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
      organizationName: credentialAttr.organization.name,
    })
  );

  const organizations = _.isUndefined(organizationsData)
    ? []
    : organizationsData.me.organizations;

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
      formatter: editAndDeleteActionFormatter,
      header: t("profile.credentialsModal.table.columns.action"),
      width: "60px",
    },
  ];

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
      : { key: values.sshKey, type: "SSH" };

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

    setIsEditing(false);
  }
  function handleOnAdd(): void {
    setIsAdding(true);
  }
  function handleOnCancel(): void {
    setIsAdding(false);
    setIsEditing(false);
  }

  return (
    <Modal
      minWidth={850}
      onClose={onClose}
      open={isOpen}
      title={t("profile.credentialsModal.title")}
    >
      <CredentialForm
        isAdding={isAdding}
        isEditing={isEditing}
        onCancel={handleOnCancel}
        onSubmit={handleSubmit}
        organizations={organizations}
      />
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
    </Modal>
  );
};

export { CredentialModal };
