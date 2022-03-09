import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useState } from "react";
import { useHistory, useParams } from "react-router-dom";

import { Table } from "components/Table";
import type { IHeaderConfig } from "components/Table/types";
import { filterSearchText } from "components/Table/utils";
import { PORTFOLIO_GROUP_QUERY } from "scenes/Dashboard/containers/TagContent/TagGroup/queries";
import { Row } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

interface IPortfolio {
  tag: {
    name: string;
    groups: { description: string; name: string }[];
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
  const [searchTextFilter, setSearchTextFilter] = useState("");

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }

  const tableHeaders: IHeaderConfig[] = [
    { dataField: "name", header: "Group Name" },
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
  const filterSearchTextDataset: IPortfolio["tag"]["groups"] = filterSearchText(
    data.tag.groups,
    searchTextFilter
  );

  return (
    <div>
      <Row>
        <Table
          customSearch={{
            customSearchDefault: searchTextFilter,
            isCustomSearchEnabled: true,
            onUpdateCustomSearch: onSearchTextChange,
            position: "right",
          }}
          dataset={filterSearchTextDataset}
          exportCsv={false}
          headers={tableHeaders}
          id={"tblGroupsTag"}
          pageSize={10}
          rowEvents={{ onClick: handleRowTagClick }}
          search={false}
        />
      </Row>
    </div>
  );
};

export { TagsGroup };
