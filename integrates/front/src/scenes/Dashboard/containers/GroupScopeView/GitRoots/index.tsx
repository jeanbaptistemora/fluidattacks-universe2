import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCloud, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import _ from "lodash";
import React, { useCallback, useState } from "react";
import { selectFilter } from "react-bootstrap-table2-filter";
import { useTranslation } from "react-i18next";

import { EnvsModal } from "./envsModal";
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
import {
  changeFormatter,
  dateFormatter,
} from "components/DataTableNext/formatters";
import { FluidIcon } from "components/FluidIcon";
import { TooltipWrapper } from "components/TooltipWrapper";
import { pointStatusFormatter } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { ButtonToolbarRow } from "styles/styledComponents";
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

export const GitRoots: React.FC<IGitRootsProps> = ({
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

  const openEditModal: () => void = useCallback((): void => {
    setManagingRoot({ mode: "EDIT" });
  }, []);

  const closeModal: () => void = useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [currentRow, setCurrentRow] =
    useState<IGitRootAttr | undefined>(undefined);

  const editDisabled: boolean =
    currentRow === undefined || currentRow.state === "INACTIVE";

  const [isManagingEnvs, setManagingEnvs] = useState(false);

  const openEnvsModal: () => void = useCallback((): void => {
    setManagingEnvs(true);
  }, []);

  const closeEnvsModal: () => void = useCallback((): void => {
    setManagingEnvs(false);
  }, []);

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
      closeEnvsModal();
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
  const handleRowSelect: (row: IGitRootAttr) => void = useCallback(
    setCurrentRow,
    [setCurrentRow]
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

  return (
    <React.Fragment>
      <h2>{t("group.scope.git.title")}</h2>
      <ButtonToolbarRow>
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
        <Can do={"api_mutations_update_git_root_mutate"}>
          <div className={"mb3"}>
            <TooltipWrapper
              id={t("group.scope.common.editTooltip.id")}
              message={t("group.scope.common.editTooltip")}
            >
              <Button disabled={editDisabled} onClick={openEditModal}>
                <FluidIcon icon={"edit"} />
                &nbsp;{t("group.scope.common.edit")}
              </Button>
            </TooltipWrapper>
          </div>
        </Can>
        <Can do={"api_mutations_update_git_environments_mutate"}>
          <div className={"mb3"}>
            <TooltipWrapper
              id={t("group.scope.git.manageEnvsTooltip.id")}
              message={t("group.scope.git.manageEnvsTooltip")}
            >
              <Button
                disabled={editDisabled}
                id={"envs-manage"}
                onClick={openEnvsModal}
              >
                <FontAwesomeIcon icon={faCloud} />
                &nbsp;{t("group.scope.git.manageEnvs")}
              </Button>
            </TooltipWrapper>
          </div>
        </Can>
      </ButtonToolbarRow>
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
                exportCsv={true}
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
                    dataField: "nickname",
                    header: "Nickname",
                    visible: checkedItems.nickname,
                  },
                  {
                    dataField: "environment",
                    header: t("group.scope.git.repo.environment"),
                    visible: checkedItems.environment,
                    width: "8%",
                  },
                  {
                    dataField: "environmentUrls",
                    formatter: formatList,
                    header: t("group.scope.git.envUrls"),
                    visible: checkedItems.environmentUrls,
                    width: "12%",
                    wrapped: true,
                  },
                  {
                    dataField: "gitignore",
                    formatter: formatList,
                    header: t("group.scope.git.filter.exclude"),
                    visible: checkedItems.gitignore,
                    width: "12%",
                    wrapped: true,
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
                    align: "center",
                    dataField: "lastStateStatusUpdate",
                    formatter: dateFormatter,
                    header: t("group.scope.common.lastStateStatusUpdate"),
                    visible: checkedItems.lastStateStatusUpdate,
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
                  {
                    align: "center",
                    dataField: "lastCloningStatusUpdate",
                    formatter: dateFormatter,
                    header: t("group.scope.common.lastCloningStatusUpdate"),
                    visible: checkedItems.lastCloningStatusUpdate,
                  },
                  {
                    dataField: "cloningStatus.message",
                    header: t("group.scope.git.repo.cloning.message"),
                    visible: checkedItems["cloningStatus.message"],
                    width: "15%",
                  },
                ]}
                id={"tblGitRoots"}
                isFilterEnabled={isFilterEnabled}
                onColumnToggle={handleChange}
                onUpdateEnableFilter={handleUpdateFilter}
                pageSize={10}
                search={true}
                selectionMode={{
                  clickToSelect: true,
                  hideSelectColumn: permissions.cannot(
                    "api_mutations_update_git_root_mutate"
                  ),
                  mode: "radio",
                  onSelect: handleRowSelect,
                }}
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
          onSubmitRepo={handleGitSubmit}
        />
      )}
      {isManagingEnvs ? (
        <EnvsModal
          initialValues={currentRow as IGitRootAttr}
          onClose={closeEnvsModal}
          onSubmit={handleEnvsSubmit}
        />
      ) : undefined}
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
