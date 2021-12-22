import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { faClock, faRocket } from "@fortawesome/free-solid-svg-icons";
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
import { formatDuration } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

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
    variables: { findingId, groupName },
  });
  const handleOnSuccess = (result: ISubmitMachineJobResult): void => {
    if (!_.isUndefined(result)) {
      if (result.submitMachineJob.success) {
        void refetch();
        msgSuccess(
          translate.t("searchFindings.tabMachine.submitJobSuccess"),
          translate.t("searchFindings.tabMachine.success")
        );
      } else {
        msgError(translate.t("searchFindings.tabMachine.errorNoCheck"));
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

  const rootNicknamesSorted: IGroupRoot[] = _.sortBy(data.group.roots, [
    (root: IGroupRoot): string => root.nickname.toLowerCase(),
  ]);
  const rootNicknames: string[] = rootNicknamesSorted
    .filter((root: IGroupRoot): boolean => root.state === "ACTIVE")
    .map((root: IGroupRoot): string => root.nickname);

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

  const tableDataset: ITableRow[] = _.isUndefined(data.finding.machineJobs)
    ? []
    : data.finding.machineJobs.map(
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
    submittingMachineJob || dataNS === NetworkStatus.refetch;

  return (
    <React.StrictMode>
      <ButtonToolbarCenter>
        {isLoading ? (
          <DropdownButton
            content={
              <div className={"tc"}>
                <FontAwesomeIcon icon={faClock} />
                &nbsp;
                {translate.t("searchFindings.tabMachine.submitting")}
              </div>
            }
            id={"submitJob"}
            items={[]}
            scrollInto={true}
          />
        ) : (
          <DropdownButton
            content={
              <div className={"tc w5"}>
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
            scrollInto={true}
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
