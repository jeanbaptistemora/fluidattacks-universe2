import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useContext, useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_ORGANIZATION_CREDENTIALS } from "./queries";
import type {
  ICredentialsAttr,
  ICredentialsData,
  IOrganizationCredentialsProps,
} from "./types";
import { getCredentialsIndex, getNonSelectableCredentialsIndex } from "./utils";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";

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
  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

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
        headers={tableHeaders}
        id={"tblOrganizationCredentials"}
        pageSize={10}
        search={false}
        selectionMode={{
          clickToSelect: true,
          hideSelectColumn: true,
          mode: "radio",
          nonSelectable: getNonSelectableCredentialsIndex(
            user.userEmail,
            filteredCredentials
          ),
          onSelect: setSelectedCredentials,
          selected: getCredentialsIndex(
            _.isUndefined(selectedCredentials) ? [] : [selectedCredentials],
            filteredCredentials
          ),
        }}
      />
    </React.StrictMode>
  );
};

export { OrganizationCredentials };
