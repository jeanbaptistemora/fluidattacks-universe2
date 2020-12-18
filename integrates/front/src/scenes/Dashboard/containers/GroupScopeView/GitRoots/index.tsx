import type { ApolloError } from "apollo-client";
import { Button } from "components/Button";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { ConfirmDialog } from "components/ConfirmDialog";
import { DataTableNext } from "components/DataTableNext";
import { EnvsModal } from "./envsModal";
import { FluidIcon } from "components/FluidIcon";
import { GitModal } from "./gitModal";
import { Glyphicon } from "react-bootstrap";
import type { GraphQLError } from "graphql";
import type { IConfirmFn } from "components/ConfirmDialog";
import type { IGitRootAttr } from "../types";
import { Logger } from "utils/logger";
import type { PureAbility } from "@casl/ability";
import React from "react";
import { authzPermissionsContext } from "utils/authz/config";
import { msgError } from "utils/notifications";
import { useAbility } from "@casl/react";
import { useMutation } from "@apollo/react-hooks";
import { useTranslation } from "react-i18next";
import {
  ADD_GIT_ROOT,
  UPDATE_GIT_ENVIRONMENTS,
  UPDATE_GIT_ROOT,
  UPDATE_ROOT_STATE,
} from "../query";
import {
  changeFormatter,
  statusFormatter,
} from "components/DataTableNext/formatters";

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

const getGlobFromRegex: (regexExpression: string) => string = (
  regexExpression
): string => regexExpression.slice(1, -1).replace(/\.\*/gu, "*");

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
  const dataset: IGitRootAttr[] = roots.map(
    (root: IGitRootAttr): IGitRootAttr => ({
      ...root,
      filter: {
        exclude: root.filter.exclude.map(getGlobFromRegex),
        include: root.filter.include.map(getGlobFromRegex),
      },
    })
  );

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const { t } = useTranslation();

  // State management
  const [isManagingRoot, setManagingRoot] = React.useState<
    { mode: "ADD" | "EDIT" } | false
  >(false);

  const openAddModal: () => void = React.useCallback((): void => {
    setManagingRoot({ mode: "ADD" });
  }, []);

  const openEditModal: () => void = React.useCallback((): void => {
    setManagingRoot({ mode: "EDIT" });
  }, []);

  const closeModal: () => void = React.useCallback((): void => {
    setManagingRoot(false);
  }, []);

  const [currentRow, setCurrentRow] = React.useState<IGitRootAttr | undefined>(
    undefined
  );

  const editDisabled: boolean =
    currentRow === undefined || currentRow.state === "INACTIVE";

  const [isManagingEnvs, setManagingEnvs] = React.useState(false);

  const openEnvsModal: () => void = React.useCallback((): void => {
    setManagingEnvs(true);
  }, []);

  const closeEnvsModal: () => void = React.useCallback((): void => {
    setManagingEnvs(false);
  }, []);

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
          case "Exception - One or more values already exist":
            msgError(t("group.scope.common.errors.duplicate"));
            break;
          default:
            msgError(t("group_alerts.error_textsad"));
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
            msgError(t("group_alerts.error_textsad"));
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
            msgError(t("group_alerts.error_textsad"));
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
      msgError(t("group_alerts.error_textsad"));
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't update root state", error);
      });
    },
  });

  // Event handlers
  const handleRowSelect: (
    row: IGitRootAttr
  ) => void = React.useCallback(setCurrentRow, [setCurrentRow]);

  const handleGitSubmit: (
    values: IGitRootAttr
  ) => Promise<void> = React.useCallback(
    async (values): Promise<void> => {
      const {
        branch,
        environment,
        filter,
        id,
        includesHealthCheck,
        url,
      } = values;

      if (currentRow === undefined) {
        await addGitRoot({
          variables: {
            branch,
            environment,
            filter: {
              exclude: filter.exclude.filter(
                (glob: string): boolean => glob.trim() !== ""
              ),
              include: filter.include,
            },
            groupName,
            includesHealthCheck,
            url,
          },
        });
      } else {
        await updateGitRoot({
          variables: {
            environment,
            filter,
            id,
            includesHealthCheck,
          },
        });
      }
    },
    [addGitRoot, currentRow, groupName, updateGitRoot]
  );

  const handleEnvsSubmit: (
    values: IGitRootAttr
  ) => Promise<void> = React.useCallback(
    async ({ environmentUrls, id }): Promise<void> => {
      await updateGitEnvs({ variables: { environmentUrls, id } });
    },
    [updateGitEnvs]
  );

  return (
    <React.Fragment>
      <h3>{t("group.scope.git.title")}</h3>
      <ButtonToolbarRow>
        <Can do={"backend_api_mutations_add_git_root_mutate"}>
          <div className={"mb3"}>
            <Button id={"git-root-add"} onClick={openAddModal}>
              <Glyphicon glyph={"plus"} />
              &nbsp;{t("group.scope.common.add")}
            </Button>
          </div>
        </Can>
        <Can do={"backend_api_mutations_update_git_root_mutate"}>
          <div className={"mb3"}>
            <Button disabled={editDisabled} onClick={openEditModal}>
              <FluidIcon icon={"edit"} />
              &nbsp;{t("group.scope.common.edit")}
            </Button>
          </div>
        </Can>
        <Can do={"backend_api_mutations_update_git_environments_mutate"}>
          <div className={"mb3"}>
            <Button disabled={editDisabled} onClick={openEnvsModal}>
              <Glyphicon glyph={"cloud"} />
              &nbsp;{t("group.scope.git.manageEnvs")}
            </Button>
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
                  id: row.id,
                  state: row.state === "ACTIVE" ? "INACTIVE" : "ACTIVE",
                },
              });
            });
          };

          return (
            <DataTableNext
              bordered={true}
              dataset={dataset}
              exportCsv={false}
              headers={[
                { dataField: "url", header: t("group.scope.git.repo.url") },
                {
                  dataField: "branch",
                  header: t("group.scope.git.repo.branch"),
                },
                {
                  dataField: "environment",
                  header: t("group.scope.git.repo.environment"),
                },
                {
                  dataField: "environmentUrls",
                  formatter: formatList,
                  header: t("group.scope.git.envUrls"),
                },
                {
                  dataField: "filter.include",
                  formatter: formatList,
                  header: t("group.scope.git.filter.include"),
                },
                {
                  dataField: "filter.exclude",
                  formatter: formatList,
                  header: t("group.scope.git.filter.exclude"),
                },
                {
                  align: "center",
                  changeFunction: handleStateUpdate,
                  dataField: "state",
                  formatter: permissions.can(
                    "backend_api_mutations_update_root_state_mutate"
                  )
                    ? changeFormatter
                    : statusFormatter,
                  header: t("group.scope.common.state"),
                },
              ]}
              id={"tblGitRoots"}
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
          );
        }}
      </ConfirmDialog>
      {isManagingRoot === false ? undefined : (
        <GitModal
          initialValues={
            isManagingRoot.mode === "EDIT" ? currentRow : undefined
          }
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
