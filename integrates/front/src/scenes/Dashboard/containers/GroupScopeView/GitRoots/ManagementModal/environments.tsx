/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { ApolloError } from "@apollo/client";
import { useMutation, useQuery } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import type { FC } from "react";
import React, { Fragment, useCallback, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import { AddEnvironment } from "./addEnvironment";

import {
  GET_ROOT_ENVIRONMENT_URLS,
  REMOVE_ENVIRONMENT_URL,
} from "../../queries";
import type { IBasicEnvironmentUrl, IFormValues } from "../../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Modal, ModalConfirm } from "components/Modal";
import { Table } from "components/Table";
import { authzPermissionsContext } from "utils/authz/config";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

interface IEnvironmentsProps {
  rootInitialValues: IFormValues;
  groupName: string;
  onClose: () => void;
  onUpdate: () => void;
}

interface IEnvironmentUrlItem extends IBasicEnvironmentUrl {
  element: JSX.Element;
}

const Environments: FC<IEnvironmentsProps> = ({
  rootInitialValues,
  groupName,
  onClose,
  onUpdate,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  const [isAddEnvModalOpen, setIsAddEnvModalOpen] = useState(false);
  const initialValues = { ...rootInitialValues, other: "", reason: "" };
  const { data, refetch } = useQuery<{
    root: { gitEnvironmentUrls: IBasicEnvironmentUrl[] };
  }>(GET_ROOT_ENVIRONMENT_URLS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load secrets", error);
      });
    },
    variables: { groupName, rootId: initialValues.id },
  });
  const [removeEnvironmentUrl] = useMutation(REMOVE_ENVIRONMENT_URL, {
    onCompleted: async (): Promise<void> => {
      await refetch();
      onUpdate();
      msgSuccess(
        t("group.scope.git.removeEnvironment.success"),
        t("group.scope.git.removeEnvironment.successTitle")
      );
    },
    onError: ({ graphQLErrors }): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.error("Couldn't remove enviroment url", error);
      });
    },
  });

  function openAddModal(): void {
    setIsAddEnvModalOpen(true);
  }
  function closeAddModal(): void {
    setIsAddEnvModalOpen(false);
  }

  const handleRemoveClick = useCallback(
    (urlId: string): void => {
      void removeEnvironmentUrl({
        variables: { groupName, rootId: initialValues.id, urlId },
      });
    },
    [groupName, initialValues.id, removeEnvironmentUrl]
  );

  const gitEnvironmentUrls = useMemo((): IEnvironmentUrlItem[] => {
    if (_.isUndefined(data) || _.isNull(data)) {
      return [];
    }

    return data.root.gitEnvironmentUrls.map(
      (gitEnvironment: IBasicEnvironmentUrl): IEnvironmentUrlItem => {
        return {
          ...gitEnvironment,
          element: (
            <ConfirmDialog title={t("group.scope.git.removeEnvironment.title")}>
              {(confirm): JSX.Element => {
                function onConfirmDelete(): void {
                  confirm((): void => {
                    handleRemoveClick(gitEnvironment.id);
                  });
                }

                return (
                  <Button
                    id={"git-root-remove-environment-url"}
                    onClick={onConfirmDelete}
                    variant={"secondary"}
                  >
                    <FontAwesomeIcon icon={faTrashAlt} />
                  </Button>
                );
              }}
            </ConfirmDialog>
          ),
        };
      }
    );
  }, [data, handleRemoveClick, t]);

  return (
    <Fragment>
      <Table
        dataset={gitEnvironmentUrls}
        exportCsv={false}
        headers={[
          {
            dataField: "url",
            header: t("group.scope.git.envUrl"),
          },
          {
            dataField: "urlType",
            header: t("group.scope.git.envUrlType"),
          },
          {
            dataField: "element",
            header: "",
            sort: false,
            visible: permissions.can(
              "api_mutations_remove_environment_url_mutate"
            ),
            width: "80px",
          },
        ]}
        id={"tblGitRootSecrets"}
        pageSize={10}
        search={false}
      />

      <Modal
        onClose={closeAddModal}
        open={isAddEnvModalOpen}
        title={t("group.scope.git.addEnvUrl")}
      >
        <AddEnvironment
          closeFunction={closeAddModal}
          groupName={groupName}
          onSubmit={refetch}
          onUpdate={onUpdate}
          rootId={initialValues.id}
        />
      </Modal>
      <ModalConfirm
        id={"add-env-url"}
        onCancel={onClose}
        onConfirm={openAddModal}
        txtConfirm={t("group.scope.git.addEnvUrl")}
      />
    </Fragment>
  );
};

export { Environments };
