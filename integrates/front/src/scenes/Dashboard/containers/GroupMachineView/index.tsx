import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { Execution } from "./execution";
import { GET_MACHINE_EXECUTIONS } from "./queries";
import type {
  IExecution,
  IGetExecutions,
  IMachineExecution,
  IRoot,
} from "./types";

import { Button } from "components/Button";
import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { formatDate, formatDuration } from "utils/formatHelpers";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const GroupMachineView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();

  // States
  const defaultCurrentRow: IExecution = {
    createdAt: "",
    duration: 0,
    findingsExecuted: [],
    jobId: "",
    name: "",
    queue: "",
    rootId: "",
    rootNickname: "",
    startedAt: "",
    stoppedAt: "",
  };

  const [currentRow, updateRow] = useState(defaultCurrentRow);

  const [isExecutionDetailsModalOpen, setExecutionDetailsModalOpen] =
    useState(false);

  const closeSeeExecutionDetailsModal: () => void = useCallback((): void => {
    setExecutionDetailsModalOpen(false);
  }, []);

  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "rootNickname",
      header: translate.t("group.machine.root"),
    },
    {
      align: "center",
      dataField: "createdAt",
      formatter: formatDate,
      header: translate.t("group.machine.date.create"),
    },
    {
      align: "center",
      dataField: "name",
      header: translate.t("group.machine.job.name"),
      wrapped: true,
    },
    {
      align: "center",
      dataField: "queue",
      header: translate.t("group.machine.job.queue"),
      wrapped: true,
    },
    {
      align: "center",
      dataField: "startedAt",
      formatter: formatDate,
      header: translate.t("group.machine.date.start"),
      wrapped: true,
    },
    {
      align: "center",
      dataField: "duration",
      formatter: formatDuration,
      header: translate.t("group.machine.date.duration"),
      wrapped: true,
    },
  ];

  const openSeeExecutionDetailsModal: (
    event: Record<string, unknown>,
    row: IExecution
  ) => void = (_0: Record<string, unknown>, row: IExecution): void => {
    updateRow(row);
    setExecutionDetailsModalOpen(true);
  };

  const handleQryErrors: (error: ApolloError) => void = ({
    graphQLErrors,
  }: ApolloError): void => {
    graphQLErrors.forEach((error: GraphQLError): void => {
      msgError(translate.t("groupAlerts.errorTextsad"));
      Logger.warning("An error occurred getting executions", error);
    });
  };

  const { data } = useQuery<IGetExecutions>(GET_MACHINE_EXECUTIONS, {
    onError: handleQryErrors,
    variables: { groupName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const executions: IExecution[] = data.group.roots.flatMap(
    (root: IRoot): IExecution[] => {
      return root.machineExecutions.map(
        (_execution: IMachineExecution): IExecution => {
          const duration =
            // @ts-expect-error operation between dates
            new Date(_execution.stoppedAt) - new Date(_execution.startedAt);

          return {
            ..._execution,
            duration,
            rootId: root.id,
            rootNickname: root.nickname,
          };
        }
      );
    }
  );

  return (
    <React.StrictMode>
      <p>{translate.t("group.machine.tableAdvice")}</p>
      <DataTableNext
        bordered={true}
        dataset={executions}
        exportCsv={true}
        headers={headersExecutionTable}
        id={"tblMachineExecutions"}
        pageSize={100}
        rowEvents={{ onClick: openSeeExecutionDetailsModal }}
        search={false}
      />
      <Modal
        headerTitle={translate.t("group.machine.executionDetailsModal.title")}
        onEsc={closeSeeExecutionDetailsModal}
        open={isExecutionDetailsModalOpen}
        size={"largeModal"}
      >
        <Execution
          createdAt={currentRow.createdAt}
          duration={currentRow.duration}
          findingsExecuted={currentRow.findingsExecuted}
          jobId={currentRow.jobId}
          name={currentRow.name}
          queue={currentRow.queue}
          rootId={currentRow.rootId}
          rootNickname={currentRow.rootNickname}
          startedAt={currentRow.startedAt}
          stoppedAt={currentRow.stoppedAt}
        />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={closeSeeExecutionDetailsModal}>
                {translate.t("group.forces.executionDetailsModal.close")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { GroupMachineView };
