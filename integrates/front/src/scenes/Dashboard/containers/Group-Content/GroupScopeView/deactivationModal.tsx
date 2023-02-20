import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { GraphQLError } from "graphql";
import type { FC, ReactNode } from "react";
import React, { StrictMode, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { GET_ROOTS_VULNS } from "./queries";
import { UpdateState } from "./updateState";

import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal } from "components/Modal";
import { Logger } from "utils/logger";

interface IDeactivationModalProps {
  groupName: string;
  rootId: string;
  onClose: () => void;
  onUpdate: () => void;
}

interface IRootsVulnsData {
  group: {
    roots: {
      id: string;
      vulnerabilities: {
        id: string;
        vulnerabilityType: string;
      }[];
    }[];
  };
}

export const DeactivationModal: FC<IDeactivationModalProps> = ({
  groupName,
  rootId,
  onClose,
  onUpdate,
}: IDeactivationModalProps): JSX.Element => {
  const { t } = useTranslation();

  const [sastVulnsToBeClosed, setSastVulnsToBeClosed] = useState<
    number | undefined
  >(0);
  const [dastVulnsToBeClosed, setDastVulnsToBeClosed] = useState<
    number | undefined
  >(0);

  const { data: rootsVulnsData } = useQuery<IRootsVulnsData>(GET_ROOTS_VULNS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load root vulnerabilities", error);
      });
    },
    variables: { groupName },
  });

  useEffect((): void => {
    const currentRootVulns = rootsVulnsData?.group.roots.find(
      (item): boolean => item.id === rootId
    );
    const currentRootSastVulns = currentRootVulns?.vulnerabilities.filter(
      (item): boolean => Object.values(item).includes("lines")
    );
    const currentRootDastVulns = currentRootVulns?.vulnerabilities.filter(
      (item): boolean => !Object.values(item).includes("lines")
    );
    setSastVulnsToBeClosed(currentRootSastVulns?.length);
    setDastVulnsToBeClosed(currentRootDastVulns?.length);
  }, [rootId, rootsVulnsData, setDastVulnsToBeClosed, setSastVulnsToBeClosed]);

  return (
    <StrictMode>
      <Modal
        onClose={onClose}
        open={true}
        title={t("group.scope.common.deactivation.title")}
      >
        <ConfirmDialog
          message={t("group.scope.common.deactivation.confirm")}
          title={t("group.scope.common.confirm")}
        >
          {(confirm): ReactNode => {
            return (
              <UpdateState
                confirm={confirm}
                dastVulnsToBeClosed={dastVulnsToBeClosed}
                groupName={groupName}
                onClose={onClose}
                onUpdate={onUpdate}
                rootId={rootId}
                sastVulnsToBeClosed={sastVulnsToBeClosed}
              />
            );
          }}
        </ConfirmDialog>
      </Modal>
    </StrictMode>
  );
};
