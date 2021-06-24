import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useTranslation } from "react-i18next";

import { renderDescription } from "./description";
import {
  handleActivationError,
  handleCreationError,
  handleDeactivationError,
  handleUpdateError,
  hasCheckedItem,
  useGitSubmit,
} from "./helpers";
import { ManagementModal } from "./Modal";
import { Container } from "./styles";

import { DeactivationModal } from "../deactivationModal";
import {
  ACTIVATE_ROOT,
  ADD_GIT_ROOT,
  DEACTIVATE_ROOT,
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
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { useStoredState } from "utils/hooks";

const formatList: (list: string[]) => JSX.Element = (list): JSX.Element => (
  <p>
    {list.map(
      (item: string): JSX.Element => (
        <React.Fragment key={item}>
          {item}
          <br />
        </React.Fragment>
      )
    )}
  </p>
);

interface IGitRootsProps {
  groupName: string;
  onUpdate: () => void;
  roots: IGitRootAttr[];
}

const GitRoots: React.FC<IGitRootsProps> = ({
  groupName,
  onUpdate,
  roots,
}: IGitRootsProps): JSX.Element => {
  // Constants
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  const canUpdateRootState: boolean = permissions.can(
    "api_mutations_update_root_state_mutate"
  );
  const nicknames: string[] = roots
    .filter((root): boolean => root.state === "ACTIVE")
    .map((root): string => root.nickname);

  // State management
  const [isManagingRoot, setManagingRoot] =
    useState<false | { mode: "ADD" | "EDIT" }>(false);

  const openAddModal: () => void = useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);

  const closeModal: () => void = useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [currentRow, setCurrentRow] =
    useState<IGitRootAttr | undefined>(undefined);

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
    "rootTableSet",
    {
      branch: true,
      "cloningStatus.message": false,
      "cloningStatus.status": true,
      environment: false,
      environmentUrls: false,
      "filter.exclude": true,
      "filter.include": true,
      lastCloningStatusUpdate: true,
      lastStateStatusUpdate: false,
      nickname: false,
      state: true,
      url: true,
    },
    localStorage
  );

  const [isFilterEnabled, setFilterEnabled] = useStoredState<boolean>(
    "rootFilters",
    false
  );

  const onfilterStatus: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("statusScopeFilter", filterVal);
  };

  const onFilterState: (filterVal: string) => void = (
    filterVal: string
  ): void => {
    sessionStorage.setItem("stateScopeFilter", filterVal);
  };

  const selectOptionsStatus = {
    FAILED: "Failed",
    OK: "Ok",
    UNKNOWN: "Unknown",
  };
  const selectOptionsState = {
    ACTIVE: "Active",
    INACTIVE: "Inactive",
  };

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

  const [deactivateRoot] = useMutation(DEACTIVATE_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeDeactivationModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      handleDeactivationError(graphQLErrors);
    },
  });

  // Event handlers
  const handleRowClick = useCallback(
    (_0: React.SyntheticEvent, row: IGitRootAttr): void => {
      if (permissions.can("api_mutations_update_git_root_mutate")) {
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

  const handleDeactivationSubmit = useCallback(
    async (rootId: string, values: Record<string, string>): Promise<void> => {
      await deactivateRoot({
        variables: {
          groupName,
          id: rootId,
          other: values.other,
          reason: values.reason,
        },
      });
    },
    [deactivateRoot, groupName]
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

  function handleUpdateFilter(): void {
    setFilterEnabled(!isFilterEnabled);
  }

  const { expandedRows, handleRowExpand, handleRowExpandAll } = useRowExpand({
    rowId: "id",
    rows: roots,
    storageKey: "gitRootsExpandedRows",
  });

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
                columnToggle={true}
                dataset={roots}
                expandRow={{
                  expandByColumnOnly: true,
                  expanded: expandedRows,
                  onExpand: handleRowExpand,
                  onExpandAll: handleRowExpandAll,
                  renderer: renderDescription,
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
                    width: "5%",
                  },
                  {
                    align: "center",
                    changeFunction: handleStateUpdate,
                    dataField: "state",
                    filter: selectFilter({
                      defaultValue: _.get(sessionStorage, "stateScopeFilter"),
                      onFilter: onFilterState,
                      options: selectOptionsState,
                    }),
                    formatter: canUpdateRootState
                      ? changeFormatter
                      : pointStatusFormatter,
                    header: t("group.scope.common.state"),
                    visible: checkedItems.state,
                    width: canUpdateRootState ? "10%" : "100px",
                    wrapped: !canUpdateRootState,
                  },
                  {
                    align: "left",
                    dataField: "cloningStatus.status",
                    filter: selectFilter({
                      defaultValue: _.get(sessionStorage, "statusScopeFilter"),
                      onFilter: onfilterStatus,
                      options: selectOptionsStatus,
                    }),
                    formatter: pointStatusFormatter,
                    header: t("group.scope.git.repo.cloning.status"),
                    visible: checkedItems["cloningStatus.status"],
                    width: "105px",
                    wrapped: true,
                  },
                ]}
                id={"tblGitRoots"}
                isFilterEnabled={isFilterEnabled}
                onColumnToggle={handleChange}
                onUpdateEnableFilter={handleUpdateFilter}
                pageSize={10}
                rowEvents={{ onClick: handleRowClick }}
                search={true}
                striped={true}
              />
            </Container>
          );
        }}
      </ConfirmDialog>
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
          onClose={closeDeactivationModal}
          onSubmit={handleDeactivationSubmit}
          rootId={deactivationModal.rootId}
        />
      ) : undefined}
    </React.Fragment>
  );
};

export { formatList, GitRoots };
