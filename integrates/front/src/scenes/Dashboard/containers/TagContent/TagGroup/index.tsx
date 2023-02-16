import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { ColumnDef, Row as TableRow } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useParams } from "react-router-dom";

import { Row } from "components/Layout";
import { Table } from "components/Table";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IPortfolio {
  tag: {
    name: string;
    groups: { description: string; name: string }[];
  };
}

interface IPortfolioViewProps {
  organizationId: string;
}

const TagsGroup: React.FC<IPortfolioViewProps> = ({
  organizationId,
}: IPortfolioViewProps): JSX.Element => {
  const { t } = useTranslation();
  const { tagName } = useParams<{ tagName: string }>();
  const { data } = useQuery<IPortfolio>(PORTFOLIO_GROUP_QUERY, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("An error occurred loading tag groups", error);
      });
    },
    variables: { organizationId, tag: tagName },
  });
  const { push } = useHistory();

  const columns: ColumnDef<{ description: string; name: string }>[] = [
    { accessorKey: "name", header: "Group Name" },
    { accessorKey: "description", header: "Description" },
  ];

  const handleRowTagClick = useCallback(
    (
      rowInfo: TableRow<{ description: string; name: string }>
    ): ((event: React.FormEvent) => void) => {
      return (event: React.FormEvent): void => {
        push(`/groups/${rowInfo.original.name.toLowerCase()}/analytics`);
        event.preventDefault();
      };
    },
    [push]
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <div>
      <Row>
        <Table
          columns={columns}
          data={data.tag.groups}
          id={"tblGroupsTag"}
          onRowClick={handleRowTagClick}
        />
      </Row>
    </div>
  );
};

export { TagsGroup };
