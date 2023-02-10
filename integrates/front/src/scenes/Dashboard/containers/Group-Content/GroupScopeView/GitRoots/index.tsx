import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type {
  ColumnDef,
  Row,
  SortingState,
  VisibilityState,
} from "@tanstack/react-table";
import _ from "lodash";
import React, { Fragment, useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";

import { renderEnvDescription } from "./envDescription";
import { changeFormatter } from "./Formatters/changeFormatter";
import { syncButtonFormatter } from "./Formatters/syncButtonFormatter";
import {
  handleActivationError,
  handleCreationError,
  handleSyncError,
  handleUpdateError,
  useGitSubmit,
} from "./helpers";
import { ManagementEnvironmentUrlsModal } from "./ManagementEnvironmentUrlsModal";
import { ManagementModal } from "./ManagementModal";
import { renderDescriptionComponent } from "./repoDescription";

import { DeactivationModal } from "../deactivationModal";
import { InternalSurfaceButton } from "../InternalSurfaceButton";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  SYNC_GIT_ROOT,
  UPDATE_GIT_ROOT,
} from "../queries";
import type {
  IEnvironmentUrl,
  IFormValues,
  IGitRootAttr,
  IGitRootData,
} from "../types";
import { Button } from "components/Button";
import { Card } from "components/Card";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IFilter } from "components/Filter";
import { Filters, useFilters } from "components/Filter";
import { Table } from "components/Table";
import type { ICellHelper } from "components/Table/types";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import { BaseStep, Tour } from "components/Tour/index";
import { UPDATE_TOURS } from "components/Tour/queries";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";
import { msgSuccess } from "utils/notifications";

interface IGitRootsProps {
  groupName: string;
  onUpdate: () => void;
  roots: IGitRootAttr[];
}

export const GitRoots: React.FC<IGitRootsProps> = ({
  groupName,
  onUpdate,
  roots: rootsAttr,
}: IGitRootsProps): JSX.Element => {
  // Constants
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  const [rootModalMessages, setRootModalMessages] = useState({
    message: "",
    type: "success",
  });
  const canSyncGitRoot: boolean = permissions.can(
    "api_mutations_sync_git_root_mutate"
  );
  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_activate_root_mutate"
  );
  const canShowModal: boolean =
    permissions.can("api_resolvers_git_root_secrets_resolve") ||
    permissions.can("api_mutations_update_git_root_mutate");
  const roots = rootsAttr.map(
    (root: IGitRootAttr): IGitRootData => ({
      ...root,
      environmentUrls: root.gitEnvironmentUrls.map(
        (gitEnvironmentUrl: IEnvironmentUrl): string => gitEnvironmentUrl.url
      ),
    })
  );
  const nicknames: string[] = roots
    .filter((root): boolean => root.state === "ACTIVE")
    .map((root): string => root.nickname);

  // State management
  const [isManagingRoot, setIsManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);
  const [isEnvironmentModalOpen, setIsEnvironmentModalOpen] = useState(false);

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );
  const enableTour = !user.tours.newRoot;
  const [runTour, setRunTour] = useState(enableTour);

  const openAddModal: () => void = useCallback((): void => {
    if (runTour) {
      setRunTour(false);
    }
    setIsManagingRoot({ mode: "ADD" });
  }, [runTour, setRunTour]);

  const closeModal: () => void = useCallback((): void => {
    if (enableTour) {
      user.setUser({
        tours: {
          newGroup: user.tours.newGroup,
          newRiskExposure: user.tours.newRiskExposure,
          newRoot: true,
        },
        userEmail: user.userEmail,
        userIntPhone: user.userIntPhone,
        userName: user.userName,
      });
    }
    setIsManagingRoot(false);
    setRootModalMessages({ message: "", type: "success" });
  }, [enableTour, user, setRootModalMessages]);

  const [currentRow, setCurrentRow] = useState<IGitRootData | undefined>(
    undefined
  );
  const [currentRowUrl, setCurrentRowUrl] = useState<
    Record<string, unknown> | undefined
  >(undefined);

  const [deactivationModal, setDeactivationModal] = useState({
    open: false,
    rootId: "",
  });

  const openDeactivationModal = useCallback((rootId: string): void => {
    setDeactivationModal({ open: true, rootId });
  }, []);

  const closeDeactivationModal = useCallback((): void => {
    setDeactivationModal({ open: false, rootId: "" });
  }, []);
  const [columnVisibility, setColumnVisibility] =
    useStoredState<VisibilityState>("tblGitRoots-visibilityState", {
      HCK: false,
      nickname: false,
    });
  const [sorting, setSorting] = useStoredState<SortingState>(
    "tblGitRoots-sortingState",
    []
  );

  // GraphQL operations
  const [updateTours] = useMutation(UPDATE_TOURS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, setRootModalMessages, "tours");
    },
  });

  const finishTour = useCallback((): void => {
    void updateTours({
      variables: {
        newGroup: user.tours.newGroup,
        newRiskExposure: user.tours.newRiskExposure,
        newRoot: true,
      },
    });
    closeModal();
  }, [closeModal, updateTours, user.tours]);

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
      finishTour();
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleCreationError(graphQLErrors, setRootModalMessages);
    },
  });

  const [updateGitRoot] = useMutation(UPDATE_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, setRootModalMessages, "root");
    },
  });

  const [activateRoot] = useMutation(ACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleActivationError(graphQLErrors);
    },
  });

  const [syncGitRoot] = useMutation(SYNC_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      msgSuccess(
        t("group.scope.git.sync.success"),
        t("group.scope.git.sync.successTitle")
      );
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleSyncError(graphQLErrors);
    },
  });

  // Event handlers
  const handleSyncClick: (row: IGitRootData) => void = (row): void => {
    void syncGitRoot({ variables: { groupName, rootId: row.id } });
  };

  function handleRowClick(
    rowInfo: Row<IGitRootData>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      if (rowInfo.original.state === "ACTIVE") {
        setCurrentRow(rowInfo.original);
        setIsManagingRoot({ mode: "EDIT" });
      }
      event.preventDefault();
    };
  }

  function handleRowUrlClick(
    rowInfo: Row<{
      createdAt: string;
      id: string;
      url: string;
      repositoryUrls: string[];
    }>
  ): (event: React.FormEvent) => void {
    return (event: React.FormEvent): void => {
      setCurrentRowUrl(rowInfo.original);
      setIsEnvironmentModalOpen(true);
      event.preventDefault();
    };
  }

  const closeEnvironmentModal = useCallback((): void => {
    setIsEnvironmentModalOpen(false);
  }, []);

  const handleGitSubmit = useGitSubmit(
    addGitRoot,
    groupName,
    isManagingRoot,
    setRootModalMessages,
    updateGitRoot
  );

  const rootsGroupedByEnvs = roots
    .filter(
      (root): boolean =>
        root.state === "ACTIVE" && root.gitEnvironmentUrls.length > 0
    )
    .reduce<Record<string, string[]>>(
      (previousValue, currentValue): Record<string, string[]> => ({
        ...previousValue,
        ...Object.fromEntries(
          currentValue.gitEnvironmentUrls.map((envUrl): [string, string[]] => [
            envUrl.url,
            [
              ...(envUrl.url in previousValue ? previousValue[envUrl.url] : []),
              currentValue.url,
            ],
          ])
        ),
      }),
      {}
    );

  const formatBoolean = useCallback(
    (value: boolean): string =>
      value
        ? t("group.scope.git.healthCheck.yes")
        : t("group.scope.git.healthCheck.no"),
    [t]
  );

  const envDataset: Record<string, unknown>[] = Object.entries(
    rootsGroupedByEnvs
  ).map(
    ([environmentUrl, repositoryUrls]): Record<string, unknown> => ({
      environmentUrl,
      repositoryUrls,
    })
  );
  const envUrlsDataSet: {
    createdAt: string;
    id: string;
    url: string;
    repositoryUrls: string[];
  }[] = roots
    .filter(
      (root): boolean =>
        root.state === "ACTIVE" && root.gitEnvironmentUrls.length > 0
    )
    .map((root): IEnvironmentUrl[] => root.gitEnvironmentUrls)
    .flatMap((envUrls): IEnvironmentUrl[] => envUrls)
    .filter(
      (envUrl, index, envUrls): boolean =>
        envUrls.findIndex((env): boolean => env.url === envUrl.url) === index
    )
    .map(
      (
        envUrl
      ): {
        createdAt: string;
        id: string;
        url: string;
        repositoryUrls: string[];
      } => {
        return {
          ...envUrl,
          repositoryUrls: rootsGroupedByEnvs[envUrl.url],
        };
      }
    );

  const handleRowExpand = useCallback(
    (row: Row<IGitRootData>): JSX.Element => {
      return renderDescriptionComponent(row.original, groupName);
    },
    [groupName]
  );

  const handleUrlRowExpand = useCallback(
    (
      row: Row<{
        createdAt: string;
        id: string;
        url: string;
        repositoryUrls: string[];
      }>
    ): JSX.Element => {
      return renderEnvDescription(row.original);
    },
    []
  );

  const managementInitialValues: IFormValues | undefined = _.isUndefined(
    currentRow
  )
    ? undefined
    : {
        branch: currentRow.branch,
        cloningStatus: currentRow.cloningStatus,
        credentials: _.isNull(currentRow.credentials)
          ? {
              auth: "",
              azureOrganization: "",
              id: "",
              isPat: false,
              key: "",
              name: "",
              password: "",
              token: "",
              type: "",
              typeCredential: "",
              user: "",
            }
          : currentRow.credentials,
        environment: currentRow.environment,
        environmentUrls: currentRow.environmentUrls,
        gitEnvironmentUrls: currentRow.gitEnvironmentUrls,
        gitignore: currentRow.gitignore,
        healthCheckConfirm: currentRow.healthCheckConfirm,
        id: currentRow.id,
        includesHealthCheck: currentRow.includesHealthCheck,
        nickname: currentRow.nickname,
        secrets: currentRow.secrets,
        state: currentRow.state,
        url: currentRow.url,
        useVpn: currentRow.useVpn,
      };

  const [filters, setFilters] = useState<IFilter<IGitRootData>[]>([
    {
      id: "nickname",
      key: "nickname",
      label: t("group.scope.git.repo.nickname"),
      type: "text",
    },
    {
      id: "branch",
      key: "branch",
      label: t("group.scope.git.repo.branch"),
      type: "text",
    },
    {
      filterFn: "caseInsensitive",
      id: "state",
      key: "state",
      label: t("group.scope.common.state"),
      selectOptions: [
        { header: "Active", value: "ACTIVE" },
        { header: "Inactive", value: "INACTIVE" },
      ],
      type: "select",
    },
    {
      filterFn: "caseInsensitive",
      id: "cloningStatus",
      key: (arg0, value): boolean => {
        if (value === "") return true;

        return value?.includes(arg0.cloningStatus.status) ?? true;
      },
      label: t("group.scope.git.repo.cloning.status"),
      selectOptions: [
        { header: "Cloning", value: "CLONING" },
        { header: "Failed", value: "FAILED" },
        { header: "N/A", value: "N/A" },
        { header: "Ok", value: "OK" },
        { header: "Queued", value: "QUEUED" },
        { header: "Unknown", value: "UNKNOWN" },
      ],
      type: "select",
    },
    {
      id: "includesHealthCheck",
      key: "includesHealthCheck",
      label: t("group.scope.common.state"),
      selectOptions: [
        { header: formatBoolean(true), value: "true" },
        { header: formatBoolean(false), value: "false" },
      ],
      type: "select",
    },
  ]);

  const filteredRoots = useFilters(roots, filters);

  return (
    <Fragment>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(confirm): React.ReactNode => {
          const handleStateUpdate: (row: IGitRootData) => void = (
            row
          ): void => {
            if (row.state === "ACTIVE") {
              openDeactivationModal(row.id);
            } else {
              confirm((): void => {
                void activateRoot({ variables: { groupName, id: row.id } });
              });
            }
          };

          return (
            <Fragment>
              <Text fw={7} mb={3} mt={4} size={"big"}>
                {t("group.scope.git.title")}
              </Text>
              <Card>
                <Table
                  columnToggle={true}
                  columnVisibilitySetter={setColumnVisibility}
                  columnVisibilityState={columnVisibility}
                  columns={(
                    [
                      {
                        accessorKey: "url",
                        enableColumnFilter: false,
                        header: String(t("group.scope.git.repo.url")),
                      },
                      {
                        accessorKey: "branch",
                        header: String(t("group.scope.git.repo.branch")),
                      },
                      {
                        accessorFn: (row): string => {
                          return _.capitalize(row.state);
                        },
                        accessorKey: "state",
                        cell: (cell: ICellHelper<IGitRootData>): JSX.Element =>
                          canUpdateRootState
                            ? changeFormatter(
                                cell.row.original,
                                handleStateUpdate
                              )
                            : statusFormatter(cell.getValue()),
                        header: String(t("group.scope.common.state")),
                      },
                      {
                        accessorFn: (row: IGitRootData): string =>
                          row.cloningStatus.status,
                        cell: (cell: ICellHelper<IGitRootData>): JSX.Element =>
                          statusFormatter(cell.getValue()),
                        header: String(
                          t("group.scope.git.repo.cloning.status")
                        ),
                      },
                      {
                        accessorFn: (row: IGitRootData): string | undefined =>
                          row.includesHealthCheck === null
                            ? undefined
                            : formatBoolean(row.includesHealthCheck),
                        header: String(
                          t("group.scope.git.healthCheck.tableHeader")
                        ),
                      },
                      {
                        accessorKey: "nickname",
                        header: String(t("group.scope.git.repo.nickname")),
                      },
                    ] as ColumnDef<IGitRootData>[]
                  ).concat(
                    canSyncGitRoot
                      ? [
                          {
                            accessorFn: (): string => "sync",
                            cell: (
                              cell: ICellHelper<IGitRootData>
                            ): JSX.Element =>
                              syncButtonFormatter(
                                cell.row.original,
                                handleSyncClick
                              ),
                            header: String(
                              t("group.scope.git.repo.cloning.sync")
                            ),
                          },
                        ]
                      : []
                  )}
                  csvHeaders={{
                    createdAt: t("group.scope.git.repo.headers.createdAt"),
                    createdBy: t("group.scope.git.repo.headers.createdBy"),
                    lastEditedAt: t(
                      "group.scope.git.repo.headers.lastEditedAt"
                    ),
                    lastEditedBy: t(
                      "group.scope.git.repo.headers.lastEditedBy"
                    ),
                  }}
                  csvName={groupName}
                  data={filteredRoots}
                  expandedRow={handleRowExpand}
                  exportCsv={true}
                  extraButtons={
                    <Fragment>
                      <Can do={"api_mutations_add_git_root_mutate"}>
                        <Tooltip
                          hide={runTour}
                          id={t("group.scope.common.addTooltip.id")}
                          tip={t("group.scope.common.addTooltip")}
                        >
                          <Button
                            id={"git-root-add"}
                            onClick={openAddModal}
                            variant={"primary"}
                          >
                            <FontAwesomeIcon icon={faPlus} />
                            &nbsp;{t("group.scope.common.add")}
                          </Button>
                        </Tooltip>
                        {runTour ? (
                          <Tour
                            run={false}
                            steps={[
                              {
                                ...BaseStep,
                                content: t("tours.addGitRoot.addButton"),
                                disableBeacon: true,
                                hideFooter: true,
                                target: "#git-root-add",
                              },
                            ]}
                          />
                        ) : undefined}
                      </Can>
                      <InternalSurfaceButton />
                    </Fragment>
                  }
                  filters={
                    <Filters filters={filters} setFilters={setFilters} />
                  }
                  id={"tblGitRoots"}
                  onRowClick={canShowModal ? handleRowClick : undefined}
                  sortingSetter={setSorting}
                  sortingState={sorting}
                />
              </Card>
            </Fragment>
          );
        }}
      </ConfirmDialog>
      {envDataset.length === 0 ? undefined : (
        <Fragment>
          <Text fw={7} mb={3} mt={4} size={"big"}>
            {t("group.scope.git.envUrls")}
          </Text>
          <Card>
            <Table
              columns={[
                {
                  accessorKey: "url",
                  header: String(t("group.scope.git.repo.url")),
                },
              ]}
              data={envUrlsDataSet}
              expandedRow={handleUrlRowExpand}
              id={"tblGitRootEnvs"}
              onRowClick={
                permissions.can(
                  "api_resolvers_git_environment_url_secrets_resolve"
                )
                  ? handleRowUrlClick
                  : undefined
              }
            />
          </Card>
          <Can do={"api_resolvers_query_environment_url_resolve"}>
            {_.isUndefined(currentRowUrl) ? undefined : (
              <ManagementEnvironmentUrlsModal
                closeModal={closeEnvironmentModal}
                groupName={groupName}
                isOpen={isEnvironmentModalOpen}
                urlId={String(currentRowUrl.id)}
              />
            )}
          </Can>
        </Fragment>
      )}
      {isManagingRoot === false ? undefined : (
        <ManagementModal
          finishTour={finishTour}
          groupName={groupName}
          initialValues={
            isManagingRoot.mode === "EDIT" ? managementInitialValues : undefined
          }
          isEditing={isManagingRoot.mode === "EDIT"}
          manyRows={false}
          modalMessages={rootModalMessages}
          nicknames={nicknames}
          onClose={closeModal}
          onSubmitRepo={handleGitSubmit}
          onUpdate={onUpdate}
          runTour={isManagingRoot.mode === "EDIT" ? false : enableTour}
        />
      )}
      {deactivationModal.open ? (
        <DeactivationModal
          groupName={groupName}
          onClose={closeDeactivationModal}
          onUpdate={onUpdate}
          rootId={deactivationModal.rootId}
        />
      ) : undefined}
    </Fragment>
  );
};
