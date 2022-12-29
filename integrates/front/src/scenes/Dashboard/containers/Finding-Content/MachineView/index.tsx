import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import { faClock, faRocket } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ColumnDef, Row } from "@tanstack/react-table";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { Execution } from "./execution";
import {
  GET_FINDING_MACHINE_JOBS,
  GET_ROOTS,
  SUBMIT_MACHINE_JOB,
} from "./queries";
import { Queue } from "./queue";
import type {
  IExecution,
  IFindingMachineJob,
  IFindingMachineJobs,
  IGroupRoot,
  ISubmitMachineJobResult,
} from "./types";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { ButtonToolbarCenter } from "styles/styledComponents";
import { formatDate, formatDuration } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const MachineView: React.FC = (): JSX.Element => {
  const { findingId, groupName } =
    useParams<{ findingId: string; groupName: string }>();

  // States
  const defaultCurrentRow: IExecution = {
    createdAt: "",
    duration: 0,
    jobId: "",
    name: "",
    priority: "",
    queue: "",
    rootId: "",
    rootNickname: "",
    startedAt: "",
    status: "",
    stoppedAt: "",
    vulnerabilities: null,
  };
  const [currentRow, setCurrentRow] = useState(defaultCurrentRow);
  const [isExecutionDetailsModalOpen, setIsExecutionDetailsModalOpen] =
    useState(false);

  const closeSeeExecutionDetailsModal: () => void = useCallback((): void => {
    setIsExecutionDetailsModalOpen(false);
  }, []);

  function openSeeExecutionDetailsModal(
    rowInfo: Row<IExecution>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setCurrentRow(rowInfo.original);
      setIsExecutionDetailsModalOpen(true);
      event.stopPropagation();
    };
  }

  // GraphQL operations
  const {
    data,
    refetch,
    networkStatus: dataNS,
  } = useQuery<IFindingMachineJobs>(GET_FINDING_MACHINE_JOBS, {
    fetchPolicy: "no-cache",
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading machine jobs", error);
      });
    },
    variables: { findingId },
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
        msgError(
          translate.t(
            result.submitMachineJob.message ||
              "searchFindings.tabMachine.errorNoCheck"
          )
        );
      }
    }
  };
  const { data: dataRoots } = useQuery<IFindingMachineJobs>(GET_ROOTS, {
    fetchPolicy: "no-cache",
    notifyOnNetworkStatusChange: true,
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        msgError(translate.t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred loading roots", error);
      });
    },
    variables: { groupName },
  });

  const handleOnError: ({ graphQLErrors }: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      switch (error.message) {
        case "Exception - Access denied or credential not found":
          msgError(translate.t("group.scope.git.sync.noCredentials"));
          break;
        case "Exception - There is already a Machine execution queued with the same parameters":
          msgError(translate.t("group.machine.alreadyQueued"));
          break;
        default:
          Logger.warning("An error occurred submitting job", error);
          msgError(translate.t("groupAlerts.errorTextsad"));
      }
    });
  };
  const [submitMachineJob, { loading: submittingMachineJob }] = useMutation(
    SUBMIT_MACHINE_JOB,
    {
      onCompleted: handleOnSuccess,
      onError: handleOnError,
    }
  );

  const [isQueueModalOpen, setIsQueueModalOpen] = useState(false);
  const closeQueueModal: () => void = useCallback((): void => {
    setIsQueueModalOpen(false);
  }, []);
  function openQueueModal(): void {
    setIsQueueModalOpen(true);
  }

  const isLoading: boolean =
    submittingMachineJob || dataNS === NetworkStatus.refetch;

  if (
    (_.isUndefined(data) || _.isEmpty(data)) &&
    (_.isUndefined(dataRoots) || _.isEmpty(dataRoots))
  ) {
    return <div />;
  }

  const rootNicknamesSorted: IGroupRoot[] = _.isUndefined(dataRoots)
    ? []
    : _.sortBy(dataRoots.group.roots, [
        (root: IGroupRoot): string => (root.nickname || "").toLowerCase(),
      ]);
  const rootNicknames: string[] = rootNicknamesSorted
    .filter((root: IGroupRoot): boolean => root.state === "ACTIVE")
    .map((root: IGroupRoot): string => root.nickname);

  const headers: ColumnDef<IExecution>[] = [
    {
      accessorKey: "status",
      header: translate.t("searchFindings.tabMachine.headerStatus"),
    },
    {
      accessorKey: "startedAt",
      cell: (cell: ICellHelper<IExecution>): string =>
        formatDate(parseFloat(cell.getValue())),
      header: translate.t("searchFindings.tabMachine.headerStartedAt"),
    },
    {
      accessorKey: "duration",
      cell: (cell: ICellHelper<IExecution>): string =>
        formatDuration(cell.getValue()),
      header: translate.t("searchFindings.tabMachine.headerDuration"),
    },
    {
      accessorKey: "rootNickname",
      header: translate.t("searchFindings.tabMachine.headerRoot"),
    },
    {
      accessorKey: "priority",
      header: translate.t("searchFindings.tabMachine.headerPriority"),
    },
  ];

  const tableDataset: IExecution[] =
    _.isUndefined(data) || _.isUndefined(data.finding.machineJobs)
      ? []
      : data.finding.machineJobs.map(
          (job: IFindingMachineJob): IExecution => ({
            ...job,
            duration:
              job.startedAt === null || job.stoppedAt === null
                ? -1
                : parseFloat(job.stoppedAt) - parseFloat(job.startedAt),
            jobId: job.id,
            priority: job.queue.endsWith("_soon")
              ? translate.t("searchFindings.tabMachine.priorityHigh")
              : translate.t("searchFindings.tabMachine.priorityNormal"),
            rootId: job.rootNickname,
            rootNickname: job.rootNickname,
            startedAt: (job.startedAt === null
              ? -1
              : parseFloat(job.startedAt)
            ).toString(),
          })
        );

  async function submitJobOnClick(
    roots: string[]
  ): Promise<FetchResult<ISubmitMachineJobResult>> {
    return submitMachineJob({
      variables: { findingId, rootNicknames: roots },
    });
  }

  return (
    <React.StrictMode>
      {_.isUndefined(dataRoots) || _.isEmpty(dataRoots) ? (
        <div />
      ) : (
        <React.StrictMode>
          <ButtonToolbarCenter>
            <Button
              disabled={isLoading}
              id={"submitJob"}
              onClick={openQueueModal}
              variant={"primary"}
            >
              <div className={"tc w5"}>
                <FontAwesomeIcon icon={isLoading ? faClock : faRocket} />
                &nbsp;
                {translate.t("searchFindings.tabMachine.submitJob")}
              </div>
            </Button>
          </ButtonToolbarCenter>
          <Modal
            onClose={closeQueueModal}
            open={isQueueModalOpen}
            title={"Queue Job"}
          >
            <Queue
              onClose={closeQueueModal}
              onSubmit={submitJobOnClick}
              rootNicknames={rootNicknames}
            />
          </Modal>
        </React.StrictMode>
      )}
      {_.isUndefined(data) || _.isEmpty(data) ? (
        <div />
      ) : (
        <React.StrictMode>
          <Table
            columns={headers}
            data={tableDataset}
            id={"tblMachineJobs"}
            onRowClick={openSeeExecutionDetailsModal}
          />
          <Modal
            onClose={closeSeeExecutionDetailsModal}
            open={isExecutionDetailsModalOpen}
            title={translate.t("group.machine.executionDetailsModal.title")}
          >
            <Execution
              createdAt={currentRow.createdAt}
              duration={currentRow.duration}
              jobId={currentRow.jobId}
              name={currentRow.name}
              priority={currentRow.priority}
              queue={currentRow.queue}
              rootId={currentRow.rootId}
              rootNickname={currentRow.rootNickname}
              startedAt={currentRow.startedAt}
              status={currentRow.status}
              stoppedAt={currentRow.stoppedAt}
              vulnerabilities={currentRow.vulnerabilities}
            />
          </Modal>
        </React.StrictMode>
      )}
    </React.StrictMode>
  );
};

export { MachineView };