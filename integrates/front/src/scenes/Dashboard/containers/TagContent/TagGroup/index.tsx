import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { IHeaderConfig } from "components/DataTableNext/types";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { Row } from "react-bootstrap";
import { useHistory, useParams } from "react-router";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IPortfolio {
  tag: {
    name: string;
    projects: Array<{description: string; name: string}>;
  };
}

const tagsGroup: React.FC = (): JSX.Element => {
  const { tagName } = useParams<{ tagName: string }>();
  const { data } = useQuery<IPortfolio>(PORTFOLIO_GROUP_QUERY, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("group_alerts.error_textsad"));
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

  const handleRowTagClick: ((event: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string }) => void) = (
    _0: React.FormEvent<HTMLButtonElement>, rowInfo: { name: string },
  ): void => {
    push(`/groups/${rowInfo.name.toLowerCase()}/analytics`);
  };

  if (_.isUndefined(data) || _.isEmpty(data)) { return <React.Fragment />; }

  return (
    <React.Fragment>
      <Row>
        <DataTableNext
          bordered={true}
          dataset={data.tag.projects}
          exportCsv={false}
          headers={tableHeaders}
          id="tblProjectsTag"
          pageSize={10}
          rowEvents={{ onClick: handleRowTagClick }}
          search={true}
        />
      </Row>
    </React.Fragment>
  );
};

export { tagsGroup as TagsGroup };
