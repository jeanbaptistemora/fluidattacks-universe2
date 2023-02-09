import { NetworkStatus, useMutation, useQuery } from "@apollo/client";
import type { ApolloError, FetchResult } from "@apollo/client";
import { faClock, faRocket } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useParams } from "react-router-dom";

import { GET_ROOTS, SUBMIT_MACHINE_JOB } from "./queries";
import { Queue } from "./queue";
import type {
  IFindingMachineJobs,
  IGroupRoot,
  ISubmitMachineJobResult,
} from "./types";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbarCenter } from "styles/styledComponents";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { translate } from "utils/translations/translate";

const MachineView: React.FC = (): JSX.Element => {
  const { findingId, groupName } = useParams<{
    findingId: string;
    groupName: string;
  }>();

  // GraphQL operations

  const handleOnSuccess = (result: ISubmitMachineJobResult): void => {
    if (!_.isUndefined(result)) {
      if (result.submitMachineJob.success) {
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
  const { data: dataRoots, networkStatus: dataNS } =
    useQuery<IFindingMachineJobs>(GET_ROOTS, {
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
  const openQueueModal = useCallback((): void => {
    setIsQueueModalOpen(true);
  }, []);

  const isLoading: boolean =
    submittingMachineJob || dataNS === NetworkStatus.refetch;

  const submitJobOnClick = useCallback(
    async (roots: string[]): Promise<FetchResult<ISubmitMachineJobResult>> => {
      return submitMachineJob({
        variables: { findingId, rootNicknames: roots },
      });
    },
    [findingId, submitMachineJob]
  );

  if (_.isUndefined(dataRoots) || _.isEmpty(dataRoots)) {
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
    </React.StrictMode>
  );
};

export { MachineView };
