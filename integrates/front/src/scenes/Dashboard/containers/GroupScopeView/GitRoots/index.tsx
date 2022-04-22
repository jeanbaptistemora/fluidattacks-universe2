import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";

import { renderEnvDescription } from "./envDescription";
import {
  filterSelectIncludesHealthCheck,
  filterSelectStatus,
  handleActivationError,
  handleCreationError,
  handleSyncError,
  handleUpdateError,
  hasCheckedItem,
  useGitSubmit,
} from "./helpers";
import { ManagementModal } from "./ManagementModal";
import { renderRepoDescription } from "./repoDescription";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import { InternalSurfaceButton } from "../InternalSurfaceButton";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  SYNC_GIT_ROOT,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
} from "../queries";
import type { IGitRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import { Table } from "components/Table";
import {
  changeFormatter,
  syncButtonFormatter,
} from "components/Table/formatters";
import { tooltipFormatter } from "components/Table/headerFormatters/tooltipFormatter";
import { useRowExpand } from "components/Table/hooks/useRowExpand";
import type { IFilterProps } from "components/Table/types";
import {
  filterSearchText,
  filterSelect,
  filterText,
} from "components/Table/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { BaseStep, Tour } from "components/Tour/index";
import { UPDATE_TOURS } from "components/Tour/queries";
import { statusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Row } from "styles/styledComponents";
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

interface IFilterSet {
  branch: string;
  includesHealthCheck?: string;
  nickname: string;
  state: string;
  status: string;
}

export const GitRoots: React.FC<IGitRootsProps> = ({
  groupName,
  onUpdate,
  roots,
}: IGitRootsProps): JSX.Element => {
  // Constants
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  const canSyncGitRoot: boolean = permissions.can(
    "api_mutations_sync_git_root_mutate"
  );
  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_activate_root_mutate"
  );
  const nicknames: string[] = roots
    .filter((root): boolean => root.state === "ACTIVE")
    .map((root): string => root.nickname);

  // State management
  const [isManagingRoot, setIsManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );
  const enableTour =
    !user.tours.newRoot && user.userEmail.endsWith("fluidattacks.com");
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
          newGroup: true,
          newRoot: true,
        },
        userEmail: user.userEmail,
        userIntPhone: user.userIntPhone,
        userName: user.userName,
      });
    }
    setIsManagingRoot(false);
  }, [enableTour, user]);

  const [currentRow, setCurrentRow] = useState<IGitRootAttr | undefined>(
    undefined
  );

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

  const [checkedItems, setCheckedItems] = useStoredState<
    Record<string, boolean>
  >(
    "gitRootsColumns",
    {
      branch: true,
      "cloningStatus.status": true,
      includesHealthCheck: false,
      state: true,
      sync: true,
      url: true,
    },
    localStorage
  );

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("rootsCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [searchEnvsTextFilter, setSearchEnvsTextFilter] = useState("");
  const [filterGroupScopeTable, setFilterGroupScopeTable] =
    useStoredState<IFilterSet>(
      "filterGroupScopeSet",
      {
        branch: "",
        includesHealthCheck: "",
        nickname: "",
        state: "",
        status: "",
      },
      localStorage
    );

  const handleUpdateCustomFilter: () => void = useCallback((): void => {
    setCustomFilterEnabled(!isCustomFilterEnabled);
  }, [isCustomFilterEnabled, setCustomFilterEnabled]);

  // GraphQL operations
  const [updateTours] = useMutation(UPDATE_TOURS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, "tours");
    },
  });

  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
      void updateTours({ variables: { newGroup: true, newRoot: true } });
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleCreationError(graphQLErrors);
    },
  });

  const [updateGitRoot] = useMutation(UPDATE_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, "root");
    },
  });

  const [updateGitEnvs] = useMutation(UPDATE_GIT_ENVIRONMENTS, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleUpdateError(graphQLErrors, "envs");
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
  const handleSyncClick: (row: Record<string, string>) => void = (
    row
  ): void => {
    void syncGitRoot({ variables: { groupName, rootId: row.id } });
  };

  const handleRowClick = useCallback(
    (_0: React.SyntheticEvent, row: IGitRootAttr): void => {
      if (row.state === "ACTIVE") {
        setCurrentRow(row);
        setIsManagingRoot({ mode: "EDIT" });
      }
    },
    []
  );

  const handleGitSubmit = useGitSubmit(
    addGitRoot,
    groupName,
    isManagingRoot,
    updateGitRoot
  );

  const handleEnvsSubmit = useCallback(
    async ({ environmentUrls, id }: IGitRootAttr): Promise<void> => {
      await updateGitEnvs({ variables: { environmentUrls, groupName, id } });
    },
    [groupName, updateGitEnvs]
  );

  function handleChange(columnName: string): void {
    if (hasCheckedItem(checkedItems, columnName)) {
      // eslint-disable-next-line no-alert -- Deliberate usage
      alert(t("validations.columns"));
      setCheckedItems({
        ...checkedItems,
        [columnName]: true,
      });
    } else {
      setCheckedItems({
        ...checkedItems,
        [columnName]: !checkedItems[columnName],
      });
    }
  }

  const rootsGroupedByEnvs = roots
    .filter(
      (root): boolean =>
        root.state === "ACTIVE" && root.environmentUrls.length > 0
    )
    .reduce<Record<string, string[]>>(
      (previousValue, currentValue): Record<string, string[]> => ({
        ...previousValue,
        ...Object.fromEntries(
          currentValue.environmentUrls.map((envUrl): [string, string[]] => [
            envUrl,
            [
              ...(envUrl in previousValue ? previousValue[envUrl] : []),
              currentValue.url,
            ],
          ])
        ),
      }),
      {}
    );

  function onSearchTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchTextFilter(event.target.value);
  }
  function onSearchEnvsTextChange(
    event: React.ChangeEvent<HTMLInputElement>
  ): void {
    setSearchEnvsTextFilter(event.target.value);
  }
  const filterSearchTextRoots: IGitRootAttr[] = filterSearchText(
    roots,
    searchTextFilter
  );

  function onNicknameChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupScopeTable(
      (value): IFilterSet => ({
        ...value,
        nickname: event.target.value,
      })
    );
  }
  const filterNicknameRoots: IGitRootAttr[] = filterText(
    roots,
    filterGroupScopeTable.nickname,
    "nickname"
  );

  function onBranchChange(event: React.ChangeEvent<HTMLInputElement>): void {
    event.persist();
    setFilterGroupScopeTable(
      (value): IFilterSet => ({
        ...value,
        branch: event.target.value,
      })
    );
  }
  const filterBranchRoots: IGitRootAttr[] = filterText(
    roots,
    filterGroupScopeTable.branch,
    "branch"
  );

  function onStateChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupScopeTable(
      (value): IFilterSet => ({
        ...value,
        state: event.target.value,
      })
    );
  }

  const formatBoolean = useCallback(
    (value: boolean): string =>
      value
        ? t("group.scope.git.healthCheck.yes")
        : t("group.scope.git.healthCheck.no"),
    [t]
  );

  const includesHealthCheckSelectOptions = Object.fromEntries([
    ["false", formatBoolean(false)],
    ["true", formatBoolean(true)],
  ]);

  const onIncludesHealthCheckChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ): void => {
    event.persist();
    setFilterGroupScopeTable(
      (value): IFilterSet => ({
        ...value,
        includesHealthCheck: event.target.value,
      })
    );
  };

  const filterStateRoots: IGitRootAttr[] = filterSelect(
    roots,
    filterGroupScopeTable.state,
    "state"
  );

  function onStatusChange(event: React.ChangeEvent<HTMLSelectElement>): void {
    event.persist();
    setFilterGroupScopeTable(
      (value): IFilterSet => ({
        ...value,
        status: event.target.value,
      })
    );
  }

  function clearFilters(): void {
    setFilterGroupScopeTable(
      (): IFilterSet => ({
        branch: "",
        includesHealthCheck: "",
        nickname: "",
        state: "",
        status: "",
      })
    );
    setSearchTextFilter("");
  }

  const filterStatusRoots: IGitRootAttr[] = filterSelectStatus(
    roots,
    filterGroupScopeTable.status
  );

  const filterHCKRoots: IGitRootAttr[] = filterSelectIncludesHealthCheck(
    roots,
    filterGroupScopeTable.includesHealthCheck ?? ""
  );

  const resultExecutions: IGitRootAttr[] = _.intersection(
    filterSearchTextRoots,
    filterNicknameRoots,
    filterBranchRoots,
    filterHCKRoots,
    filterStateRoots,
    filterStatusRoots
  );

  const { expandedRows, handleRowExpand, handleRowExpandAll } = useRowExpand({
    rowId: "id",
    rows: resultExecutions,
    storageKey: "gitRootsExpandedRows",
  });

  const customFiltersProps: IFilterProps[] = [
    {
      defaultValue: filterGroupScopeTable.nickname,
      onChangeInput: onNicknameChange,
      placeholder: "Nickname",
      tooltipId: "group.scope.git.filtersTooltips.nickname.id",
      tooltipMessage: "group.scope.git.filtersTooltips.nickname",
      type: "text",
    },
    {
      defaultValue: filterGroupScopeTable.branch,
      onChangeInput: onBranchChange,
      placeholder: "Branch",
      tooltipId: "group.scope.git.filtersTooltips.branch.id",
      tooltipMessage: "group.scope.git.filtersTooltips.branch",
      type: "text",
    },
    {
      defaultValue: filterGroupScopeTable.state,
      onChangeSelect: onStateChange,
      placeholder: "State",
      selectOptions: {
        ACTIVE: "Active",
        INACTIVE: "Inactive",
      },
      tooltipId: "group.scope.git.filtersTooltips.state.id",
      tooltipMessage: "group.scope.git.filtersTooltips.state",
      type: "select",
    },
    {
      defaultValue: filterGroupScopeTable.status,
      onChangeSelect: onStatusChange,
      placeholder: "Status",
      selectOptions: {
        FAILED: "Failed",
        OK: "Ok",
        UNKNOWN: "Unknown",
      },
      tooltipId: "group.scope.git.filtersTooltips.status.id",
      tooltipMessage: "group.scope.git.filtersTooltips.status",
      type: "select",
    },
    {
      defaultValue: filterGroupScopeTable.includesHealthCheck ?? "",
      onChangeSelect: onIncludesHealthCheckChange,
      placeholder: t("group.scope.git.filtersTooltips.healthCheck.placeholder"),
      selectOptions: includesHealthCheckSelectOptions,
      tooltipId: "group.scope.git.filtersTooltips.healthCheck.id",
      tooltipMessage: "group.scope.git.filtersTooltips.healthCheck.text",
      type: "select",
    },
  ];

  const envDataset: Record<string, unknown>[] = Object.entries(
    rootsGroupedByEnvs
  ).map(
    ([environmentUrl, repositoryUrls]): Record<string, unknown> => ({
      environmentUrl,
      repositoryUrls,
    })
  );
  const filterEnvSearchTextDataset: Record<string, unknown>[] =
    filterSearchText(envDataset, searchEnvsTextFilter);

  return (
    <React.Fragment>
      <h2>{t("group.scope.git.title")}</h2>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(confirm): React.ReactNode => {
          const handleStateUpdate: (row: Record<string, string>) => void = (
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
            <Container>
              <Table
                clearFiltersButton={clearFilters}
                columnToggle={true}
                customFilters={{
                  customFiltersProps,
                  isCustomFilterEnabled,
                  onUpdateEnableCustomFilter: handleUpdateCustomFilter,
                  resultSize: {
                    current: resultExecutions.length,
                    total: roots.length,
                  },
                }}
                customSearch={{
                  customSearchDefault: searchTextFilter,
                  isCustomSearchEnabled: true,
                  onUpdateCustomSearch: onSearchTextChange,
                  position: "right",
                }}
                dataset={resultExecutions}
                expandRow={{
                  expandByColumnOnly: true,
                  expanded: expandedRows,
                  onExpand: handleRowExpand,
                  onExpandAll: handleRowExpandAll,
                  renderer: renderRepoDescription(groupName),
                  showExpandColumn: true,
                }}
                exportCsv={true}
                extraButtons={
                  <Row>
                    <Can do={"api_mutations_add_git_root_mutate"}>
                      <TooltipWrapper
                        id={t("group.scope.common.addTooltip.id")}
                        message={t("group.scope.common.addTooltip")}
                      >
                        <Button
                          id={"git-root-add"}
                          onClick={openAddModal}
                          variant={"secondary"}
                        >
                          <FontAwesomeIcon icon={faPlus} />
                          &nbsp;{t("group.scope.common.add")}
                        </Button>
                        {runTour ? (
                          <Tour
                            run={true}
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
                      </TooltipWrapper>
                    </Can>
                    <InternalSurfaceButton />
                  </Row>
                }
                headers={[
                  {
                    dataField: "url",
                    header: t("group.scope.git.repo.url"),
                    visible: checkedItems.url,
                    wrapped: true,
                  },
                  {
                    dataField: "branch",
                    header: t("group.scope.git.repo.branch"),
                    visible: checkedItems.branch,
                  },
                  {
                    changeFunction: handleStateUpdate,
                    dataField: "state",
                    formatter: canUpdateRootState
                      ? changeFormatter
                      : statusFormatter,
                    header: t("group.scope.common.state"),
                    visible: checkedItems.state,
                    width: canUpdateRootState ? "130px" : "100px",
                  },
                  {
                    dataField: "cloningStatus.status",
                    formatter: statusFormatter,
                    header: t("group.scope.git.repo.cloning.status"),
                    visible: checkedItems["cloningStatus.status"],
                    width: "105px",
                  },
                  {
                    dataField: "includesHealthCheck",
                    formatter: formatBoolean,
                    header: t("group.scope.git.healthCheck.tableHeader"),
                    headerFormatter: tooltipFormatter,
                    tooltipDataField: t(
                      "group.scope.git.healthCheck.titleTooltip"
                    ),
                    visible: _.isUndefined(checkedItems.includesHealthCheck)
                      ? false
                      : checkedItems.includesHealthCheck,
                    width: "45px",
                  },
                  {
                    changeFunction: handleSyncClick,
                    dataField: "sync",
                    formatter: syncButtonFormatter,
                    header: t("group.scope.git.repo.cloning.sync"),
                    visible: canSyncGitRoot && checkedItems.sync,
                    width: "15px",
                  },
                ]}
                id={"tblGitRoots"}
                onColumnToggle={handleChange}
                pageSize={10}
                rowEvents={{ onClick: handleRowClick }}
                search={false}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      <br />
      {envDataset.length === 0 ? undefined : (
        <React.Fragment>
          <h2 className={"mb0 pb0"}>{t("group.scope.git.envUrls")}</h2>
          <div className={"flex flex-wrap nt2"}>
            <Table
              customSearch={{
                customSearchDefault: searchEnvsTextFilter,
                isCustomSearchEnabled: true,
                onUpdateCustomSearch: onSearchEnvsTextChange,
                position: "right",
              }}
              dataset={filterEnvSearchTextDataset}
              expandRow={{
                expandByColumnOnly: true,
                renderer: renderEnvDescription,
                showExpandColumn: true,
              }}
              exportCsv={false}
              headers={[
                {
                  dataField: "environmentUrl",
                  header: t("group.scope.git.repo.url"),
                },
              ]}
              id={"tblGitRootEnvs"}
              pageSize={10}
              search={false}
            />
          </div>
        </React.Fragment>
      )}
      {isManagingRoot === false ? undefined : (
        <ManagementModal
          groupName={groupName}
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
          nicknames={nicknames}
          onClose={closeModal}
          onSubmitEnvs={handleEnvsSubmit}
          onSubmitRepo={handleGitSubmit}
          runTour={enableTour}
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
    </React.Fragment>
  );
};
