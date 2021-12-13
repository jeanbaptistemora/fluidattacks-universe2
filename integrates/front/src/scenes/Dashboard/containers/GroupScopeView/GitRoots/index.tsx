import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { useTranslation } from "react-i18next";

import { renderEnvDescription } from "./envDescription";
import {
  filterSelectStatus,
  handleActivationError,
  handleCreationError,
  handleUpdateError,
  hasCheckedItem,
  useGitSubmit,
} from "./helpers";
import { ManagementModal } from "./ManagementModal";
import { renderRepoDescription } from "./repoDescription";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
} from "../queries";
import type { IGitRootAttr } from "../types";
import { Button } from "components/Button";
import { ConfirmDialog } from "components/ConfirmDialog";
import type { IConfirmFn } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { changeFormatter } from "components/DataTableNext/formatters";
import { useRowExpand } from "components/DataTableNext/hooks/useRowExpand";
import type { IFilterProps } from "components/DataTableNext/types";
import {
  filterSearchText,
  filterSelect,
  filterText,
} from "components/DataTableNext/utils";
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";

interface IGitRootsProps {
  groupName: string;
  onUpdate: () => void;
  roots: IGitRootAttr[];
}

interface IFilterSet {
  branch: string;
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

  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_activate_root_mutate"
  );
  const nicknames: string[] = roots
    .filter((root): boolean => root.state === "ACTIVE")
    .map((root): string => root.nickname);

  // State management
  const [isManagingRoot, setManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);

  const openAddModal: () => void = useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);

  const closeModal: () => void = useCallback((): void => {
    setManagingRoot(false);
  }, []);

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
      state: true,
      url: true,
    },
    localStorage
  );

  const [isCustomFilterEnabled, setCustomFilterEnabled] =
    useStoredState<boolean>("rootsCustomFilters", false);

  const [searchTextFilter, setSearchTextFilter] = useState("");
  const [filterGroupScopeTable, setFilterGroupScopeTable] =
    useStoredState<IFilterSet>(
      "filterGroupScopeSet",
      {
        branch: "",
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
  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
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

  // Event handlers
  const handleRowClick = useCallback(
    (_0: React.SyntheticEvent, row: IGitRootAttr): void => {
      if (
        permissions.can("api_mutations_update_git_root_mutate") &&
        row.state === "ACTIVE"
      ) {
        setCurrentRow(row);
        setManagingRoot({ mode: "EDIT" });
      }
    },
    [permissions]
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

  const resultExecutions: IGitRootAttr[] = _.intersection(
    filterSearchTextRoots,
    filterNicknameRoots,
    filterBranchRoots,
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
  ];

  return (
    <React.Fragment>
      <h2>{t("group.scope.git.title")}</h2>
      <ConfirmDialog title={t("group.scope.common.confirm")}>
        {(confirm: IConfirmFn): React.ReactNode => {
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
              <DataTableNext
                bordered={true}
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
                }}
                dataset={resultExecutions}
                expandRow={{
                  expandByColumnOnly: true,
                  expanded: expandedRows,
                  onExpand: handleRowExpand,
                  onExpandAll: handleRowExpandAll,
                  renderer: renderRepoDescription,
                  showExpandColumn: true,
                }}
                exportCsv={true}
                extraButtons={
                  <Can do={"api_mutations_add_git_root_mutate"}>
                    <div className={"mb3"}>
                      <TooltipWrapper
                        id={t("group.scope.common.addTooltip.id")}
                        message={t("group.scope.common.addTooltip")}
                      >
                        <Button id={"git-root-add"} onClick={openAddModal}>
                          <FontAwesomeIcon icon={faPlus} />
                          &nbsp;{t("group.scope.common.add")}
                        </Button>
                      </TooltipWrapper>
                    </div>
                  </Can>
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
                    align: "center",
                    changeFunction: handleStateUpdate,
                    dataField: "state",
                    formatter: canUpdateRootState
                      ? changeFormatter
                      : pointStatusFormatter,
                    header: t("group.scope.common.state"),
                    visible: checkedItems.state,
                    width: canUpdateRootState ? "10%" : "100px",
                  },
                  {
                    align: "left",
                    dataField: "cloningStatus.status",
                    formatter: pointStatusFormatter,
                    header: t("group.scope.git.repo.cloning.status"),
                    visible: checkedItems["cloningStatus.status"],
                    width: "105px",
                  },
                ]}
                id={"tblGitRoots"}
                onColumnToggle={handleChange}
                pageSize={10}
                rowEvents={{ onClick: handleRowClick }}
                search={false}
                striped={true}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
      <br />
      <h2>{t("group.scope.git.envUrls")}</h2>
      <DataTableNext
        bordered={true}
        dataset={Object.entries(rootsGroupedByEnvs).map(
          ([environmentUrl, repositoryUrls]): Record<string, unknown> => ({
            environmentUrl,
            repositoryUrls,
          })
        )}
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
        search={true}
        striped={true}
      />
      {isManagingRoot === false ? undefined : (
        <ManagementModal
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
          nicknames={nicknames}
          onClose={closeModal}
          onSubmitEnvs={handleEnvsSubmit}
          onSubmitRepo={handleGitSubmit}
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
