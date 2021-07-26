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
import { timeFromUnix } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const formatDuration = (value: number): string => {
  if (value < 0) {
    return "-";
  }

  const secondsInAnHour: number = 3600;

  return `${value / secondsInAnHour}`;
};

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
      dataField: "startedAt",
      formatter: timeFromUnix,
      header: translate.t("searchFindings.tabMachine.headerStartedAt"),
      width: "10%",
    },
    {
      align: "center",
      dataField: "duration",
      formatter: formatDuration,
      header: translate.t("searchFindings.tabMachine.headerDuration"),
      width: "10%",
    },
    {
      align: "center",
      dataField: "rootNickname",
      header: translate.t("searchFindings.tabMachine.headerRoot"),
      width: "30%",
    },
  ];

  const tableDataset: ITableRow[] = data.finding.machineJobs.map(
    (job: IFindingMachineJob): ITableRow => ({
      duration:
        job.startedAt === null || job.stoppedAt === null
          ? -1
          : parseFloat(job.stoppedAt) - parseFloat(job.startedAt),
      rootNickname: job.rootNickname,
      startedAt: job.startedAt === null ? -1 : parseFloat(job.startedAt),
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
