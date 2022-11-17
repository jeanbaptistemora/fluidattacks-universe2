/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import type { ColumnDef } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { ActionButtons } from "./ActionButtons";
import { CredentialsModal } from "./CredentialsModal";
import { GET_ORGANIZATION_CREDENTIALS, REMOVE_CREDENTIALS } from "./queries";
import type {
  ICredentialsAttr,
  ICredentialsData,
  IOrganizationCredentialsProps,
  IRemoveCredentialsResultAttr,
} from "./types";

import { GET_ROOTS } from "../GroupScopeView/queries";
import { Table } from "components/Table";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const OrganizationCredentials: React.FC<IOrganizationCredentialsProps> = ({
  organizationId,
}: IOrganizationCredentialsProps): JSX.Element => {
  const { t } = useTranslation();

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
          switch (error.message) {
            default:
              msgError(t("groupAlerts.errorTextsad"));
              Logger.warning("An error occurred adding credentials", error);
          }
        });
      },
      refetchQueries: [GET_ORGANIZATION_CREDENTIALS, GET_ROOTS],
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
  const credentialsAttrs = _.isUndefined(data)
    ? []
    : data.organization.credentials;
  const credentials: ICredentialsData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialsAttr): ICredentialsData => ({
      ...credentialAttr,
      formattedType: formatType(credentialAttr),
    })
  );

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

  const removeCredentials = useCallback((): void => {
    if (!_.isUndefined(selectedCredentials)) {
      void handleRemoveCredentials({
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
            selectedCredentials={selectedCredentials[0]}
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
