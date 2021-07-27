import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faRocket } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_FINDING_MACHINE_JOBS, SUBMIT_MACHINE_JOB } from "./queries";
import type {
  IFindingMachineJob,
  IFindingMachineJobs,
  IGroupRoot,
  ISubmitMachineJobResult,
  ITableRow,
} from "./types";

import { DataTableNext } from "components/DataTableNext";
import { timeFromUnix } from "components/DataTableNext/formatters";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { DropdownButton, MenuItem } from "components/DropdownButton";
import { ButtonToolbarCenter } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const formatDuration = (value: number): string => {
  if (value < 0) {
    return "-";
  }

  const miliSecondsInAnHour: number = 3600000;

  return `${(value / miliSecondsInAnHour).toFixed(2)}`;
};

const loadingNetworkStatuses: NetworkStatus[] = [
  NetworkStatus.loading,
  NetworkStatus.fetchMore,
  NetworkStatus.refetch,
  NetworkStatus.setVariables,
];

const MachineView: React.FC = (): JSX.Element => {
  const { findingId, groupName } =
    useParams<{ findingId: string; groupName: string }>();

  // GraphQL operations
  const {
    data,
    refetch,
    networkStatus: dataNS,
  } = useQuery<IFindingMachineJobs>(GET_FINDING_MACHINE_JOBS, {
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading machine jobs", error);
      });
    },
    pollInterval: 10000,
    variables: { findingId, groupName },
  });
  const handleOnSuccess = (result: ISubmitMachineJobResult): void => {
    if (!_.isUndefined(result)) {
      if (result.submitMachineJob.success) {
        msgSuccess(
          translate.t("searchFindings.tabMachine.submitJobSuccess"),
          translate.t("searchFindings.tabMachine.success")
        );
        void refetch();
      }
    }
  };
  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      Logger.warning("An error occurred submitting job", error);
      msgError(translate.t("groupAlerts.errorTextsad"));
    });
  };
  const [submitMachineJob, { loading: submittingMachineJob }] = useMutation(
    SUBMIT_MACHINE_JOB,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const rootNicknames: string[] = data.group.roots.map(
    (root: IGroupRoot): string => root.nickname
  );

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
      width: "60%",
    },
    {
      align: "center",
      dataField: "priority",
      header: translate.t("searchFindings.tabMachine.headerPriority"),
      width: "10%",
    },
  ];

  const tableDataset: ITableRow[] = data.finding.machineJobs.map(
    (job: IFindingMachineJob): ITableRow => ({
      duration:
        job.startedAt === null || job.stoppedAt === null
          ? -1
          : parseFloat(job.stoppedAt) - parseFloat(job.startedAt),
      priority: job.queue.endsWith("_soon")
        ? translate.t("searchFindings.tabMachine.priorityHigh")
        : translate.t("searchFindings.tabMachine.priorityNormal"),
      rootNickname: job.rootNickname,
      startedAt: job.startedAt === null ? -1 : parseFloat(job.startedAt),
      status: job.status,
    })
  );

  const submitJobOnClick = (rootNickname: string): void => {
    void submitMachineJob({ variables: { findingId, rootNickname } });
  };

  const isLoading: boolean =
    submittingMachineJob || loadingNetworkStatuses.includes(dataNS);

  return (
    <React.StrictMode>
      <ButtonToolbarCenter>
        {isLoading ? undefined : (
          <DropdownButton
            content={
              <div className={"tc"}>
                <FontAwesomeIcon icon={faRocket} />
                &nbsp;
                {translate.t("searchFindings.tabMachine.submitJob")}
              </div>
            }
            id={"submitJob"}
            items={rootNicknames.map(
              (nickname: string): JSX.Element => (
                <MenuItem
                  eventKey={nickname}
                  itemContent={<span>{nickname}</span>}
                  key={nickname}
                  // eslint-disable-next-line react/jsx-no-bind
                  onClick={submitJobOnClick}
                />
              )
            )}
            scrollInto={false}
          />
        )}
      </ButtonToolbarCenter>

      <DataTableNext
        bordered={false}
        dataset={tableDataset}
        exportCsv={false}
        headers={headers}
        id={"tblMachineJobs"}
        pageSize={1000}
        search={false}
      />
    </React.StrictMode>
  );
};

export { MachineView };
