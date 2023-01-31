import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useCallback, useContext, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { Table } from "components/Table";
import { ActionButtons } from "scenes/Dashboard/containers/Organization-Content/OrganizationCredentialsView/ActionButtons";
import { CredentialsModal } from "scenes/Dashboard/containers/Organization-Content/OrganizationCredentialsView/CredentialsModal";
import {
  GET_ORGANIZATION_CREDENTIALS,
  REMOVE_CREDENTIALS,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationCredentialsView/queries";
import type {
  ICredentialsAttr,
  ICredentialsData,
  IOrganizationCredentialsProps,
  IRemoveCredentialsResultAttr,
} from "scenes/Dashboard/containers/Organization-Content/OrganizationCredentialsView/types";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const OrganizationCredentials: React.FC<IOrganizationCredentialsProps> = ({
  organizationId,
}: IOrganizationCredentialsProps): JSX.Element => {
  const { t } = useTranslation();
  const { userEmail }: IAuthContext = useContext(authContext);

  // Permissions
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRemove: boolean = permissions.can(
    "api_mutations_remove_credentials_mutate"
  );
  const canUpadate: boolean = permissions.can(
    "api_mutations_update_credentials_mutate"
  );

  // States
  const [selectedCredentials, setSelectedCredentials] = useState<
    ICredentialsData[]
  >([]);
  const [isCredentialsModalOpen, setIsCredentialsModalOpen] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const [isEditing, setIsEditing] = useState(false);

  // GraphQl mutations
  const [handleRemoveCredentials, { loading: isRemoving }] =
    useMutation<IRemoveCredentialsResultAttr>(REMOVE_CREDENTIALS, {
      onCompleted: (result: IRemoveCredentialsResultAttr): void => {
        if (result.removeCredentials.success) {
          msgSuccess(
            t("organization.tabs.credentials.alerts.removeSuccess"),
            t("groupAlerts.titleSuccess")
          );
          setSelectedCredentials([]);
        }
      },
      onError: (errors: ApolloError): void => {
        errors.graphQLErrors.forEach((error: GraphQLError): void => {
          if (error.message) {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning("An error occurred adding credentials", error);
          }
        });
      },
      refetchQueries: [
        {
          query: GET_ORGANIZATION_CREDENTIALS,
          variables: {
            organizationId,
          },
        },
      ],
    });

  // GraphQl queries
  const { data } = useQuery<{
    organization: { credentials: ICredentialsAttr[] };
  }>(GET_ORGANIZATION_CREDENTIALS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load organization credentials", error);
      });
    },
    variables: {
      organizationId,
    },
  });

  const formatType = useCallback(
    (value: ICredentialsAttr): string => {
      if (value.type === "HTTPS") {
        if (value.isToken) {
          if (value.isPat && value.azureOrganization !== null) {
            return t(
              "organization.tabs.credentials.credentialsModal.form.auth.azureToken"
            );
          }

          return t(
            "organization.tabs.credentials.credentialsModal.form.auth.token"
          );
        }

        return t(
          "organization.tabs.credentials.credentialsModal.form.auth.user"
        );
      }

      return value.type;
    },
    [t]
  );

  // Format data
  const credentialsAttrs = useMemo(
    (): ICredentialsAttr[] =>
      _.isUndefined(data) ? [] : data.organization.credentials,
    [data]
  );
  const credentials: ICredentialsData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialsAttr): ICredentialsData => ({
      ...credentialAttr,
      formattedType: formatType(credentialAttr),
    })
  );
  const shouldDisplayGithubButton = useMemo((): boolean => {
    return (
      credentialsAttrs.filter(
        (credential: ICredentialsAttr): boolean =>
          credential.type === "OAUTH" &&
          credential.oauthType === "GITHUB" &&
          credential.owner.toLowerCase() === userEmail.toLowerCase()
      ).length === 0
    );
  }, [credentialsAttrs, userEmail]);

  const shouldDisplayBitbucketButton = useMemo((): boolean => {
    return (
      credentialsAttrs.filter(
        (credential: ICredentialsAttr): boolean =>
          credential.type === "OAUTH" &&
          credential.oauthType === "BITBUCKET" &&
          credential.owner.toLowerCase() === userEmail.toLowerCase()
      ).length === 0
    );
  }, [credentialsAttrs, userEmail]);

  const shouldDisplayGitlabButton = useMemo((): boolean => {
    return (
      credentialsAttrs.filter(
        (credential: ICredentialsAttr): boolean =>
          credential.type === "OAUTH" &&
          credential.oauthType === "GITLAB" &&
          credential.owner.toLowerCase() === userEmail.toLowerCase()
      ).length === 0
    );
  }, [credentialsAttrs, userEmail]);

  const shouldDisplayAzureButton = useMemo((): boolean => {
    return (
      credentialsAttrs.filter(
        (credential: ICredentialsAttr): boolean =>
          credential.type === "OAUTH" &&
          credential.oauthType === "AZURE" &&
          credential.owner.toLowerCase() === userEmail.toLowerCase()
      ).length === 0
    );
  }, [credentialsAttrs, userEmail]);

  // Handle actions
  const openCredentialsModalToAdd = useCallback((): void => {
    setIsCredentialsModalOpen(true);
    setIsAdding(true);
  }, []);
  const openCredentialsModalToEdit = useCallback((): void => {
    setIsCredentialsModalOpen(true);
    setIsEditing(true);
  }, []);
  const closeCredentialsModal = useCallback((): void => {
    setIsCredentialsModalOpen(false);
    setIsAdding(false);
    setIsEditing(false);
  }, []);

  const removeCredentials = useCallback(async (): Promise<void> => {
    if (!_.isUndefined(selectedCredentials)) {
      await handleRemoveCredentials({
        variables: {
          credentialsId: selectedCredentials[0].id,
          organizationId,
        },
      });
    }
  }, [handleRemoveCredentials, selectedCredentials, organizationId]);

  // Table config
  const tableColumns: ColumnDef<ICredentialsData>[] = [
    {
      accessorKey: "name",
      header: t("organization.tabs.credentials.table.columns.name"),
    },
    {
      accessorKey: "formattedType",
      header: t("organization.tabs.credentials.table.columns.type"),
    },
    {
      accessorKey: "owner",
      header: t("organization.tabs.credentials.table.columns.owner"),
    },
  ];

  return (
    <React.StrictMode>
      <Table
        columns={tableColumns}
        data={credentials}
        extraButtons={
          <ActionButtons
            isAdding={isAdding}
            isEditing={isEditing}
            isRemoving={isRemoving}
            onAdd={openCredentialsModalToAdd}
            onEdit={openCredentialsModalToEdit}
            onRemove={removeCredentials}
            organizationId={organizationId}
            selectedCredentials={selectedCredentials[0]}
            shouldDisplayAzureButton={shouldDisplayAzureButton}
            shouldDisplayBitbucketButton={shouldDisplayBitbucketButton}
            shouldDisplayGithubButton={shouldDisplayGithubButton}
            shouldDisplayGitlabButton={shouldDisplayGitlabButton}
          />
        }
        id={"tblOrganizationCredentials"}
        rowSelectionSetter={
          canRemove || canUpadate ? setSelectedCredentials : undefined
        }
        rowSelectionState={selectedCredentials}
        selectionMode={"radio"}
      />
      {isCredentialsModalOpen ? (
        <CredentialsModal
          isAdding={isAdding}
          isEditing={isEditing}
          onClose={closeCredentialsModal}
          organizationId={organizationId}
          selectedCredentials={selectedCredentials}
          setSelectedCredentials={setSelectedCredentials}
        />
      ) : undefined}
    </React.StrictMode>
  );
};

export { OrganizationCredentials };
