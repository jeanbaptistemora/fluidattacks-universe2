import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useCallback, useContext, useState } from "react";
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
import { getCredentialsIndex, getNonSelectableCredentialsIndex } from "./utils";

import { GET_ROOTS } from "../GroupScopeView/queries";
import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

const OrganizationCredentials: React.FC<IOrganizationCredentialsProps> = ({
  organizationId,
}: IOrganizationCredentialsProps): JSX.Element => {
  const { t } = useTranslation();
  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  // States
  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [selectedCredentials, setSelectedCredentials] = useState<
    ICredentialsAttr | undefined
  >();
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
          setSelectedCredentials(undefined);
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

  // Format data
  const credentialsAttrs = _.isUndefined(data)
    ? []
    : data.organization.credentials;
  const credentials: ICredentialsData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialsAttr): ICredentialsData => ({
      ...credentialAttr,
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
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  const removeCredentials = useCallback((): void => {
    if (!_.isUndefined(selectedCredentials)) {
      void handleRemoveCredentials({
        variables: {
          credentialsId: selectedCredentials.id,
          organizationId,
        },
      });
    }
  }, [handleRemoveCredentials, selectedCredentials, organizationId]);

  // Filter data
  const filteredCredentials: ICredentialsData[] = filterSearchText(
    credentials,
    searchTextFilter
  );

  // Table config
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "name",
      header: t("organization.tabs.credentials.table.columns.name"),
      wrapped: true,
    },
    {
      dataField: "type",
      header: t("organization.tabs.credentials.table.columns.type"),
      wrapped: true,
    },
    {
      dataField: "owner",
      header: t("organization.tabs.credentials.table.columns.owner"),
      wrapped: true,
    },
  ];
  const nonSelectableCredentialsIndex = getNonSelectableCredentialsIndex(
    user.userEmail,
    filteredCredentials
  );
  const hideActions =
    nonSelectableCredentialsIndex.length === filteredCredentials.length;

  return (
    <React.StrictMode>
      <Table
        customSearch={{
          customSearchDefault: searchTextFilter,
          isCustomSearchEnabled: true,
          onUpdateCustomSearch: onSearchTextChange,
          position: "right",
        }}
        dataset={filteredCredentials}
        exportCsv={false}
        extraButtons={
          // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
          hideActions ? undefined : (
            <ActionButtons
              isAdding={isAdding}
              isEditing={isEditing}
              isRemoving={isRemoving}
              onAdd={openCredentialsModalToAdd}
              onEdit={openCredentialsModalToEdit}
              onRemove={removeCredentials}
              selectedCredentials={selectedCredentials}
            />
          )
        }
        headers={tableHeaders}
        id={"tblOrganizationCredentials"}
        pageSize={10}
        search={false}
        selectionMode={{
          clickToSelect: true,
          hideSelectColumn: hideActions,
          mode: "radio",
          nonSelectable: nonSelectableCredentialsIndex,
          onSelect: setSelectedCredentials,
          selected: getCredentialsIndex(
            _.isUndefined(selectedCredentials) ? [] : [selectedCredentials],
            filteredCredentials
          ),
        }}
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
