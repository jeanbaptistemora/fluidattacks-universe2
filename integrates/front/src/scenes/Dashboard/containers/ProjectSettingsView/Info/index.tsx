import type { ApolloError } from "apollo-client";
import { DataTableNext } from "components/DataTableNext";
import { GET_GROUP_DATA } from "scenes/Dashboard/containers/ProjectSettingsView/queries";
import type { GraphQLError } from "graphql";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import React from "react";
import _ from "lodash";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";
import { useParams } from "react-router-dom";
import { useQuery } from "@apollo/react-hooks";
import { Flex, LastProjectSetting } from "styles/styledComponents";

const GroupInformation: React.FC = (): JSX.Element => {
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
    return <div />;
  }
  const attributesDataset: { attribute: string; value: string }[] = [
    {
      attribute: "Language",
      // Next annotations needed as DB queries use "any" type
      // eslint-disable-next-line @typescript-eslint/restrict-template-expressions, @typescript-eslint/no-unsafe-member-access
      value: translate.t(`searchFindings.infoTable.${data.project.language}`),
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
          <h2>{translate.t("searchFindings.infoTable.title")}</h2>
        </Flex>
        <DataTableNext
          bordered={true}
          dataset={attributesDataset}
          exportCsv={false}
          headers={tableHeaders}
          id={"tblGroupInfo"}
          pageSize={15}
          search={false}
          striped={true}
        />
      </LastProjectSetting>
    </React.StrictMode>
  );
};

export { GroupInformation };
