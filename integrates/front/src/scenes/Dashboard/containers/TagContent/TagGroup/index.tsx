import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import React from "react";
import { Row } from "styles/styledComponents";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useQuery } from "@apollo/react-hooks";
import { useHistory, useParams } from "react-router";

interface IPortfolio {
  tag: {
    name: string;
    projects: { description: string; name: string }[];
  };
}

const TagsGroup: React.FC = (): JSX.Element => {
  const { tagName } = useParams<{ tagName: string }>();
  const { data } = useQuery<IPortfolio>(PORTFOLIO_GROUP_QUERY, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.error("An error occurred loading tag groups", error);
      });
    },
    variables: { tag: tagName },
  });
  const { push } = useHistory();

  const tableHeaders: IHeaderConfig[] = [
    { dataField: "name", header: "Project Name" },
    { dataField: "description", header: "Description" },
  ];

  const handleRowTagClick: (
    event: React.FormEvent<HTMLButtonElement>,
    rowInfo: { name: string }
  ) => void = (
    _0: React.FormEvent<HTMLButtonElement>,
    rowInfo: { name: string }
  ): void => {
    push(`/groups/${rowInfo.name.toLowerCase()}/analytics`);
  };

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  return (
    <div>
      <Row>
        <DataTableNext
          bordered={true}
          dataset={data.tag.projects}
          exportCsv={false}
          headers={tableHeaders}
          id={"tblProjectsTag"}
          pageSize={10}
          rowEvents={{ onClick: handleRowTagClick }}
          search={true}
        />
      </Row>
    </div>
  );
};

export { TagsGroup };
