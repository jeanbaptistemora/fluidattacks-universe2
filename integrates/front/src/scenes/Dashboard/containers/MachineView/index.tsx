import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_FINDING_MACHINE_JOBS } from "./queries";
import type {
  IFindingMachineJob,
  IFindingMachineJobs,
  ITableRow,
} from "./types";

import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const MachineView: React.FC = (): JSX.Element => {
  const { findingId } = useParams<{ findingId: string }>();

  // GraphQL operations
  const { data } = useQuery<IFindingMachineJobs>(GET_FINDING_MACHINE_JOBS, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading machine jobs", error);
      });
    },
    variables: { findingId },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const headers: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "status",
      header: translate.t("searchFindings.tabMachine.headerStatus"),
      width: "10%",
    },
    {
      align: "center",
      dataField: "name",
      header: translate.t("searchFindings.tabMachine.headerName"),
      width: "30%",
    },
  ];

  const tableDataset: ITableRow[] = data.finding.machineJobs.map(
    (job: IFindingMachineJob): ITableRow => ({
      name: job.name,
      status: job.status,
    })
  );

  return (
    <React.StrictMode>
      <DataTableNext
        bordered={true}
        dataset={tableDataset}
        exportCsv={true}
        headers={headers}
        id={"tblMachineJobs"}
        pageSize={100}
        search={true}
      />
    </React.StrictMode>
  );
};

export { MachineView };
