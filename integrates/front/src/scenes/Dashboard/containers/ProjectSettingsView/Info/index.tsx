import { useQuery } from "@apollo/react-hooks";
import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { IHeaderConfig } from "components/DataTableNext/types";
import { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import {
  Flex,
  LastProjectSetting,
} from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const groupInformation: React.FC = (): JSX.Element => {
  const { projectName } = useParams<{ projectName: string }>();

  const { data } = useQuery(GET_GROUP_DATA, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.error_text"));
        Logger.warning("An error occurred getting group data", error);
      });
    },
    variables: { groupName: projectName },
  });
  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }
  const attributesDataset: Array<{ attribute: string; value: string }> = [
    {
      attribute: "Language",
      value: translate.t(`search_findings.info_table.${data.project.language}`),
    },
  ];
  const tableHeaders: IHeaderConfig[] = [
    {
      dataField: "attribute",
      header: "Attribute",
    },
    {
      dataField: "value",
      header: "Value",
    },
  ];

  return (
    <React.StrictMode>
      <LastProjectSetting>
        <Flex>
          <h2>
            {translate.t("search_findings.info_table.title")}
          </h2>
        </Flex>
        <DataTableNext
          bordered={true}
          dataset={attributesDataset}
          exportCsv={false}
          search={false}
          headers={tableHeaders}
          id="tblGroupInfo"
          pageSize={15}
          striped={true}
        />
      </LastProjectSetting>
    </React.StrictMode>
  );
};

export { groupInformation as GroupInformation };
