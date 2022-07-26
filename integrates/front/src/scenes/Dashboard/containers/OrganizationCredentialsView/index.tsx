import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
// https://github.com/mixpanel/mixpanel-js/issues/321
// eslint-disable-next-line import/no-named-default
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_ORGANIZATION_CREDENTIALS } from "./queries";
import type {
  ICredentialAttr,
  ICredentialData,
  IOrganizationCredentialsProps,
} from "./types";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { Logger } from "utils/logger";

const OrganizationCredentials: React.FC<IOrganizationCredentialsProps> = ({
  organizationId,
}: IOrganizationCredentialsProps): JSX.Element => {
  const { t } = useTranslation();

  // States
  const [searchTextFilter, setSearchTextFilter] = useState("");

  // GraphQl queries
  const { data } = useQuery<{
    organization: { credentials: ICredentialAttr[] };
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
  const credentials: ICredentialData[] = credentialsAttrs.map(
    (credentialAttr: ICredentialAttr): ICredentialData => ({
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
  const filteredCredentials: ICredentialData[] = filterSearchText(
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
      />
    </React.StrictMode>
  );
};

export { OrganizationCredentials };
