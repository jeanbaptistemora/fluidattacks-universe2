import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useParams } from "react-router-dom";

import { GET_MACHINE_EXECUTIONS } from "./queries";
import type {
  IExecution,
  IGetExecutions,
  IMachineExecution,
  IRoot,
} from "./types";

import { DataTableNext } from "components/DataTableNext";
import type { IHeaderConfig } from "components/DataTableNext/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";
import { translate } from "utils/translations/translate";

const transformDuration = (value: number): string => {
  if (value < 0) {
    return "-";
  }
  const secondsInMili = 1000;
  const factor = 60;

  const seconds = Math.trunc(value / secondsInMili);
  const minutes = Math.trunc(seconds / factor);
  const ss = seconds % factor;
  const hh = Math.trunc(minutes / factor);
  const mm = minutes % factor;
  const hhStr = hh.toString().length === 1 ? `0${hh}` : hh.toString();
  const mmStr = hh.toString().length === 1 ? `0${mm}` : mm.toString();
  const ssStr = ss.toString().length === 1 ? `0${ss}` : ss.toString();

  return `${hhStr}:${mmStr}:${ssStr}`;
};

const GroupMachineView: React.FC = (): JSX.Element => {
  const { groupName } = useParams<{ groupName: string }>();
  const headersExecutionTable: IHeaderConfig[] = [
    {
      align: "center",
      dataField: "rootNickname",
      header: translate.t("group.machine.root"),
    },
    {
      align: "center",
      dataField: "createdAt",
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
      header: translate.t("group.machine.date.start"),
      wrapped: true,
    },
    {
      align: "center",
      dataField: "duration",
      header: translate.t("group.machine.date.duration"),
      wrapped: true,
    },
  ];

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
            new Date(_execution.startedAt) - new Date(_execution.stoppedAt);

          return {
            ..._execution,
            duration: transformDuration(duration),
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
        search={false}
      />
    </React.StrictMode>
  );
};

export { GroupMachineView };
