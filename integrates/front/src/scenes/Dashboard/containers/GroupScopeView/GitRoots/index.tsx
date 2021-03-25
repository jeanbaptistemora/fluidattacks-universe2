import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { EnvsModal } from "./envsModal";
import { FluidIcon } from "components/FluidIcon";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { GitModal } from "./gitModal";
import type { GraphQLError } from "graphql";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IGitRootAttr } from "../types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import { TooltipWrapper } from "components/TooltipWrapper";
import _ from "lodash";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";
import { selectFilter } from "react-bootstrap-table2-filter";
import style from "./index.css";
import { track } from "mixpanel-browser";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { useStoredState } from "utils/hooks";
import { useTranslation } from "react-i18next";
import {
  ADD_GIT_ROOT,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
  UPDATE_ROOT_STATE,
} from "../query";
import React, { useCallback, useState } from "react";
import {
  changeFormatter,
  dateFormatter,
  statusFormatter,
} from "components/DataTableNext/formatters";
import { faCloud, faPlus } from "@fortawesome/free-solid-svg-icons";

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

  const nicknames: string[] = roots.map((root): string => root.nickname);

  // State management
  const [isManagingRoot, setManagingRoot] = useState<
    false | { mode: "ADD" | "EDIT" }
  >(false);

  const openAddModal: () => void = useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);

  const openEditModal: () => void = useCallback((): void => {
    setManagingRoot({ mode: "EDIT" });
  }, []);

  const closeModal: () => void = useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [currentRow, setCurrentRow] = useState<IGitRootAttr | undefined>(
    undefined
  );

  const editDisabled: boolean =
    currentRow === undefined || currentRow.state === "INACTIVE";

  const [isManagingEnvs, setManagingEnvs] = useState(false);

  const openEnvsModal: () => void = useCallback((): void => {
    setManagingEnvs(true);
  }, []);

  const closeEnvsModal: () => void = useCallback((): void => {
    setManagingEnvs(false);
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
  // Const []
  const selectOptionsStatus: optionSelectFilterProps[] = [
    { label: "Failed", value: "FAILED" },
    { label: "Ok", value: "OK" },
    { label: "Unknown", value: "UNKNOWN" },
  ];
  const selectOptionsState: optionSelectFilterProps[] = [
    { label: "Active", value: "ACTIVE" },
    { label: "Inactive", value: "INACTIVE" },
  ];

  // GraphQL operations
  const [addGitRoot] = useMutation(ADD_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.git.errors.invalid"));
            break;
          case "Exception - Active root with the same Nickname already exists":
            msgError(t("group.scope.common.errors.duplicateNickname"));
            break;
          case "Exception - Active root with the same URL/branch already exists":
            msgError(t("group.scope.common.errors.duplicateUrl"));
            break;
          case "Exception - Root name should not be included in the exception pattern":
            msgError(t("group.scope.git.errors.rootInGitignore"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't add git roots", error);
        }
      });
    },
  });

  const [updateGitRoot] = useMutation(UPDATE_GIT_ROOT, {
    onCompleted: (): void => {
      onUpdate();
      closeModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.git.errors.invalid"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't update git root", error);
        }
      });
    },
  });

  const [updateGitEnvs] = useMutation(UPDATE_GIT_ENVIRONMENTS, {
    onCompleted: (): void => {
      onUpdate();
      closeEnvsModal();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Error empty value is not valid":
            msgError(t("group.scope.git.errors.invalid"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't update git envs", error);
        }
      });
    },
  });

  const [updateRootState] = useMutation(UPDATE_ROOT_STATE, {
    onCompleted: (): void => {
      onUpdate();
      setCurrentRow(undefined);
    },
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        switch (error.message) {
          case "Exception - Active root with the same URL/branch already exists":
            msgError(t("group.scope.common.errors.duplicateUrl"));
            break;
          default:
            msgError(t("groupAlerts.errorTextsad"));
            Logger.error("Couldn't update root state", error);
        }
      });
    },
  });

  // Event handlers
  const handleRowSelect: (
    row: IGitRootAttr
  ) => void = useCallback(setCurrentRow, [setCurrentRow]);

  const handleGitSubmit: (values: IGitRootAttr) => Promise<void> = useCallback(
    async (values): Promise<void> => {
      const {
        branch,
        environment,
        gitignore,
        id,
        includesHealthCheck,
        nickname,
        url,
      } = values;

      if (isManagingRoot !== false) {
        if (isManagingRoot.mode === "ADD") {
          track("AddGitRoot");
          await addGitRoot({
            variables: {
              branch,
              environment,
              gitignore,
              groupName,
              includesHealthCheck,
              nickname,
              url,
            },
          });
        } else {
          track("EditGitRoot");
          await updateGitRoot({
            variables: {
              environment,
              gitignore,
              groupName,
              id,
              includesHealthCheck,
              nickname,
            },
          });
        }
      }
    },
    [addGitRoot, groupName, isManagingRoot, updateGitRoot]
  );

  const handleEnvsSubmit: (values: IGitRootAttr) => Promise<void> = useCallback(
    async ({ environmentUrls, id }): Promise<void> => {
      await updateGitEnvs({ variables: { environmentUrls, groupName, id } });
    },
    [groupName, updateGitEnvs]
  );

  function handleChange(columnName: string): void {
    if (
      Object.values(checkedItems).filter((val: boolean): boolean => val)
        .length === 1 &&
      checkedItems[columnName]
    ) {
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
        <Can do={"backend_api_mutations_add_git_root_mutate"}>
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
        <Can do={"backend_api_mutations_update_git_root_mutate"}>
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
        <Can do={"backend_api_mutations_update_git_environments_mutate"}>
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
            confirm((): void => {
              void updateRootState({
                variables: {
                  groupName,
                  id: row.id,
                  state: row.state === "ACTIVE" ? "INACTIVE" : "ACTIVE",
                },
              });
            });
          };

          return (
            <div className={style.container}>
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
                    visible: checkedItems["filter.exclude"],
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
                    formatter: permissions.can(
                      "backend_api_mutations_update_root_state_mutate"
                    )
                      ? changeFormatter
                      : statusFormatter,
                    header: t("group.scope.common.state"),
                    visible: checkedItems.state,
                    width: "10%",
                  },
                  {
                    align: "center",
                    dataField: "lastStateStatusUpdate",
                    formatter: dateFormatter,
                    header: t("group.scope.common.lastStateStatusUpdate"),
                    visible: checkedItems.lastStateStatusUpdate,
                  },
                  {
                    align: "center",
                    dataField: "cloningStatus.status",
                    filter: selectFilter({
                      defaultValue: _.get(sessionStorage, "statusScopeFilter"),
                      onFilter: onfilterStatus,
                      options: selectOptionsStatus,
                    }),
                    formatter: statusFormatter,
                    header: t("group.scope.git.repo.cloning.status"),
                    visible: checkedItems["cloningStatus.status"],
                    width: "15%",
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
                  },
                ]}
                id={"tblGitRoots"}
                isFilterEnabled={isFilterEnabled}
                onColumnToggle={handleChange}
                onUpdateEnableFilter={handleUpdateFilter}
                pageSize={15}
                search={true}
                selectionMode={{
                  clickToSelect: true,
                  hideSelectColumn: permissions.cannot(
                    "backend_api_mutations_update_git_root_mutate"
                  ),
                  mode: "radio",
                  onSelect: handleRowSelect,
                }}
                striped={true}
              />
            </div>
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <GitModal
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
          nicknames={nicknames}
          onClose={closeModal}
          onSubmit={handleGitSubmit}
        />
      )}
      {isManagingEnvs ? (
        <EnvsModal
          initialValues={currentRow as IGitRootAttr}
          onClose={closeEnvsModal}
          onSubmit={handleEnvsSubmit}
        />
      ) : undefined}
    </React.Fragment>
  );
};
